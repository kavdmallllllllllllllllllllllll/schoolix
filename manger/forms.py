from django import forms

class AttendanceUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='تحميل ملف الحضور', 
        help_text='يجب أن يكون الملف بتنسيق Excel (.xlsx أو .xls)'
    )
