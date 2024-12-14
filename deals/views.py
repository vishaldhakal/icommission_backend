from rest_framework import generics, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from .models import Deal, PortfolioSettings, DealType
from .serializers import (
    DealSerializer, 
    PortfolioSettingsSerializer,
    DealAnalyticsSerializer
)
import csv
from django.http import HttpResponse
from io import StringIO
from datetime import datetime
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
from rest_framework.parsers import MultiPartParser
from django.db.models import Q

class DealFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')
    type = filters.CharFilter(field_name='type', method='filter_type')
    status = filters.CharFilter(field_name='status', method='filter_status')
    category = filters.CharFilter(field_name='category', method='filter_category')
    search = filters.CharFilter(method='filter_search')
    
    def filter_type(self, queryset, name, value):
        if value == 'ALL' or not value:
            return queryset
        return queryset.filter(type=value)

    def filter_status(self, queryset, name, value):
        if value == 'ALL' or not value:
            return queryset
        return queryset.filter(status=value)

    def filter_category(self, queryset, name, value):
        if value == 'ALL' or not value:
            return queryset
        return queryset.filter(category=value)

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(file__icontains=value) |
            Q(name__icontains=value) |
            Q(company__icontains=value) |
            Q(transaction_address__icontains=value)
        )
    
    class Meta:
        model = Deal
        fields = ['date_from', 'date_to', 'type', 'status', 'category', 'search']

class DealListCreateView(generics.ListCreateAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DealFilter
    search_fields = ['file', 'name', 'company', 'transaction_address']
    ordering_fields = ['date', 'purchased_commission_amount', 'purchase_price']

class DealRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser])
def import_deals(request):
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES['file']
    
    if not file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        decoded_file = file.read().decode('utf-8-sig')  # Handle BOM
        reader = csv.reader(StringIO(decoded_file))
        
        with transaction.atomic():
            created_count = 0
            updated_count = 0
            
            # Skip header row
            next(reader)
            
            for row in reader:
                try:
                    if len(row) < 18:  # Ensure we have all required fields
                        continue
                        
                    # Extract values from row
                    file_id = row[0]
                    date = row[1]
                    category = row[2]
                    transaction_address = row[3]
                    name = row[4]
                    company = row[5]
                    deal_type = row[6]
                    purchased_commission = row[7]
                    purchase_price = row[8]
                    closing_date = row[10]  # Index 10 for closing date
                    agent_commission = row[13]  # Index 13 for agent commission
                    status_value = row[16]  # Index 16 for status
                    internal_notes = row[17] if len(row) > 17 else ''

                    # Clean monetary values only if available as otherwise 0 if string is there or empty
                    if purchased_commission and purchased_commission != '-':
                        purchased_commission = float(purchased_commission.replace('$', '').replace(',', ''))
                    else:
                        purchased_commission = 0

                    if purchase_price and purchase_price != '-':
                        purchase_price = float(purchase_price.replace('$', '').replace(',', ''))
                    else:
                        purchase_price = 0

                    if agent_commission and agent_commission != '-':
                        agent_commission = float(agent_commission.replace('$', '').replace(',', ''))
                    else:
                        agent_commission = 0

                    if closing_date and closing_date != '-':
                        closing_date = datetime.strptime(closing_date, '%m/%d/%Y').date()
                    else:
                        closing_date = None

                    deal, created = Deal.objects.update_or_create(
                        file=file_id,
                        defaults={
                            'date': datetime.strptime(date, '%m/%d/%Y').date(),
                            'category': category,
                            'transaction_address': transaction_address,
                            'name': name,
                            'company': company,
                            'type': deal_type,
                            'purchased_commission_amount': purchased_commission,
                            'purchase_price': purchase_price,
                            'closing_date': closing_date,
                            'agent_commission': agent_commission,
                            'status': status_value.upper(),
                            'internal_notes': internal_notes
                        }
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                except (ValueError, IndexError) as e:
                    return Response(
                        {'error': f'Error processing row: {str(e)}\nRow data: {row}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Exception as e:
                    return Response(
                        {'error': f'Unexpected error: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        return Response({
            'message': 'Import successful',
            'created': created_count,
            'updated': updated_count
        }, status=status.HTTP_200_OK)

    except UnicodeDecodeError:
        return Response(
            {'error': 'Invalid file encoding. Please use UTF-8.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def export_deals(request):
    deals = Deal.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="deals_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'File', 'Date', 'Category', 'Transaction Address', 'Name', 'Company',
        'Type', 'Purchased commission amount', 'Purchase price', 'Term/days',
        'Closing date', 'Discount fee/income', 'Rate', 'Agent Commission',
        'Advance Ratio', 'Countdown', 'Status', 'Internal Notes'
    ])
    
    for deal in deals:
        writer.writerow([
            deal.file,
            deal.date.strftime('%m/%d/%Y'),
            deal.category,
            deal.transaction_address,
            deal.name,
            deal.company,
            deal.type.replace('_', ' ').title(),
            f"{deal.purchased_commission_amount:,.2f}",
            f"{deal.purchase_price:,.2f}",
            deal.term_days,
            deal.closing_date.strftime('%m/%d/%Y'),
            f"{deal.discount_fee:,.2f}",
            f"{deal.rate:.2f}%",
            f"{deal.agent_commission:,.2f}",
            f"{deal.advance_ratio:.2f}%" if deal.advance_ratio else "",
            deal.countdown,
            deal.status.title(),
            deal.internal_notes
        ])
    
    return response

@api_view(['GET'])
def get_analytics(request):
    deals = Deal.objects.all()
    closed_deals = deals.filter(status='CLOSED')
    
    # Calculate average term days
    total_term_days = sum(deal.term_days for deal in deals)
    avg_term_days = float(total_term_days / len(deals)) if deals else 0
    
    analytics_data = {
        'total_purchased_commission': float(deals.aggregate(
            total=Sum('purchased_commission_amount')
        )['total'] or 0),
        'total_purchase_price': float(deals.aggregate(
            total=Sum('purchase_price')
        )['total'] or 0),
        'average_repayment_term': round(float(avg_term_days), 2),
        'total_discount_fee': float(sum(deal.discount_fee for deal in deals)),
        'average_apr': float(sum(deal.rate for deal in deals) / len(deals) if deals else 0),
        'total_agent_commission': float(deals.aggregate(
            total=Sum('agent_commission')
        )['total'] or 0),
        'average_advance_ratio': float(sum(deal.advance_ratio for deal in deals) / len(deals) if deals else 0),
        'total_income_realized': float(sum(deal.discount_fee for deal in closed_deals)),
        'total_repayments_received': closed_deals.count(),
        'portfolio_breakdown': get_portfolio_breakdown(deals)
    }
    
    serializer = DealAnalyticsSerializer(analytics_data)
    return Response(serializer.data)

def get_portfolio_breakdown(deals):
    exposure_basis = float(PortfolioSettings.objects.first().exposure_basis if PortfolioSettings.objects.exists() else 1500000)
    
    breakdown = {}
    for deal_type in DealType.choices:
        type_deals = deals.filter(type=deal_type[0])
        total_amount = float(sum(deal.purchased_commission_amount for deal in type_deals))
        ratio = float((total_amount / exposure_basis) * 100 if exposure_basis else 0)
        
        breakdown[deal_type[0]] = {
            'amount': total_amount,
            'ratio': round(ratio, 2)
        }
    
    return breakdown

class PortfolioSettingsListCreateView(generics.ListCreateAPIView):
    queryset = PortfolioSettings.objects.all()
    serializer_class = PortfolioSettingsSerializer

class PortfolioSettingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PortfolioSettings.objects.all()
    serializer_class = PortfolioSettingsSerializer
