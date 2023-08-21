from django import forms
from . import models

class UAVForm(forms.ModelForm):

    class Meta:
        model = models.UAV
        fields = ('brand', 'model', 'weigth', 'category')
        labels = {
            'brand': 'Brand',
            'model': 'Model',
            'weigth': 'Weigth',
            'category': 'Category',
        }
    


class RentalForm(forms.ModelForm):
    class Meta:
        model = models.Rental
        fields = ('uav', 'user', 'start_date', 'end_date')
        labels = {
            'uav': 'UAV',
            'user': 'Rental User',
            'start_date': 'Start Date and Time',
            'end_date': 'End Date and Time',
        }
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    
    def clean(self):
        cleaned_data = super().clean()
        uav = cleaned_data.get('uav')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        print("DEBUG: Checking UAV ID:", uav.id if uav else "None")  # Debug print
        print("DEBUG: Checking between dates:", start_date, "and", end_date)  # Debug print

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("The start date must be before the end date.")
    
        # Check for overlapping rentals
        overlapping_rentals = models.Rental.objects.filter(
            uav=uav,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if overlapping_rentals.exists():
            print("DEBUG: Overlap found!")  # Debug print
            raise forms.ValidationError("This UAV is already rented for the specified date range.")
        else:
            print("DEBUG: No overlap found.")  # Debug print

        return cleaned_data

