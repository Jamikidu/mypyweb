from django import forms

# 클라이언트가 화면에서 입력
class AddProductForm(forms.Form):
    quantity = forms.IntegerField() #수량
    is_update = forms.BooleanField(required=False,
                                   initial=False, widget=forms.HiddenInput)