import csv
import os
from crm.models import Recipient, LogisticsTrackingSystem, HelpRequest, Coordinator, Supplier, MonitoringAgency, HumanitarianAidSystem

def run():
    file_path = os.path.join(os.path.dirname(__file__), 'humanitarian_aid_dataset_500.csv')
    print(f"Opening file: {file_path}")
    try:
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            row_count = 0
            for row in reader:
                try:
                    print(f"Processing row: {row}")
                    
                    recipient, created = Recipient.objects.get_or_create(
                        recipientid=row['recipientid'],
                        defaults={
                            'organizationName': row['organizationName'],
                            'contactinfo': row['contactinfo'],
                            'address': row.get('Recipient Address', ''),
                            'phone_number': row.get('Recipient Phone Number', ''),
                            'email': row.get('Recipient Email', '')
                        }
                    )
                    print(f"Recipient processed: {recipient}")
                    
                    logistics, created = LogisticsTrackingSystem.objects.get_or_create(
                        trackingId=row['trackingId'],
                        defaults={
                            'status': row['status'] == 'True',
                            'wheredelivery': row['wheredelivery']
                        }
                    )
                    print(f"Logistics processed: {logistics}")
                    
                    help_request, created = HelpRequest.objects.get_or_create(
                        requestId=row['requestId'],
                        defaults={
                            'requestDetails': row['requestDetails'],
                            'status': row['requestStatus'] == 'True'
                        }
                    )
                    print(f"Help request processed: {help_request}")
                    
                    coordinator, created = Coordinator.objects.get_or_create(
                        coordinatorId=row['coordinatorId'],
                        defaults={
                            'name': row['coordinatorName'],
                            'role': row['role'],
                            'phone_number': row.get('Coordinator Phone Number', ''),
                            'email': row.get('Coordinator Email', '')
                        }
                    )
                    print(f"Coordinator processed: {coordinator}")
                    
                    supplier, created = Supplier.objects.get_or_create(
                        supplierId=row['supplierId'],
                        defaults={
                            'name': row['supplierName'],
                            'contactInfo': row['supplierContactInfo'],
                            'address': row.get('Supplier Address', ''),
                            'phone_number': row.get('Supplier Phone Number', ''),
                            'email': row.get('Supplier Email', '')
                        }
                    )
                    print(f"Supplier processed: {supplier}")
                    
                    monitoring_agency, created = MonitoringAgency.objects.get_or_create(
                        monitoryagencyId=row['monitoryagencyId'],
                        defaults={
                            'contactInfo': row['monitoryAgencyContactInfo'],
                            'name': row['monitoryagencyName'],
                            'address': row.get('Monitoring Agency Address', ''),
                            'phone_number': row.get('Monitoring Agency Phone Number', ''),
                            'email': row.get('Monitoring Agency Email', '')
                        }
                    )
                    print(f"Monitoring agency processed: {monitoring_agency}")
                    
                    humanitarian_aid_system, created = HumanitarianAidSystem.objects.get_or_create(
                        humanitarianCoordinatorId=row['humanitarianCoordinatorId'],
                        defaults={
                            'name': 'Humanitarian Aid System',
                            'assignedRegion': row['assignedRegion'],
                            'requestId': help_request
                        }
                    )
                    print(f"Humanitarian aid system processed: {humanitarian_aid_system}")
                    
                    row_count += 1
                    print(f"Processed row: {row}")
                except Exception as row_error:
                    print(f"Error processing row: {row} - {row_error}")
            print(f"Total rows processed: {row_count}")
    except Exception as e:
        print(f"Error processing file: {e}")