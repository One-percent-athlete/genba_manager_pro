from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,SetPasswordForm
from django import forms
from .models import Profile, Genba, DailyReport

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>記号、スペースなし、150文字以下</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>ユーザー名と一致しない</li><li>8文字以上</li><li>数字のみ不可</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = '確認パスワード'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>再度パスワード入力</small></span>'
    
class UserProfileForm(forms.ModelForm):
	CHOICE = [
       	('下請け', '下請け'),
        ('正社員', '正社員'),
        ('管理', '管理'),]
	fullname = forms.CharField(label="お名前", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'フルネームスペースなし'}))
	phone = forms.CharField(label="携帯電話番号", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'07012345678'}))
	note = forms.CharField(label="備考欄", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'注意事項'}))
	contract_type = forms.ChoiceField(label="雇用形態", choices=CHOICE, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	is_active = forms.BooleanField(label="現役中", required=False)

	class Meta:
		model = Profile
		fields = ('fullname', 'phone', 'note', 'contract_type', 'is_active')

class GenbaForm(forms.ModelForm):
	COLORS = (
		('#808080', '灰色'),
        ('#ff6961', '赤色'),
        ('#ffb480', '橙色'),
        ('#f8f38d', '黄色'),
        ('#42d6a4', '緑色'),
        ('#08cad1', '水色'),
        ('#59adf6', '青色'),
        ('#9d94ff', '紫色'),
        ('#c780e8', '桃色'),
    )
	head_person = forms.Select(attrs={"class":"form-select"})
	attendees = forms.ModelMultipleChoiceField(label="同行者", queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple)
	name = forms.Select(attrs={"class":"form-select", "placeholder": "現場名"})
	client = forms.Select(attrs={"class":"form-select", "placeholder": "取引先"})
	address = forms.CharField(label="場所", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	color = forms.ChoiceField(label="カレンダー表示色", choices=COLORS, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	job_description = forms.CharField(label="作業内容", max_length=100,required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	note = forms.CharField(label="連絡事項", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	finished = forms.BooleanField(label="完了", required=False)
	start_date = forms.DateField(label='作業開始日', widget=forms.DateInput(attrs={'type': 'date'}))
	end_date = forms.DateField(label='作業終了日', widget=forms.DateInput(attrs={'type': 'date'}))

	class Meta:
		model = Genba
		fields = ('head_person', 'attendees', 'name', 'client', 'address', 'job_description','note', 'finished', 'start_date', 'end_date', 'color')
		labels = {
			'head_person':'職長',
			'attendees': '同行者',
			'name': '現場名',
			'client': '取引先',
		}

class DailyReportForm(forms.ModelForm):
	PAYMENT_TYPES = (
        ('現金','現金'),
        ('カード', 'カード'),
        ('電子マネー', '電子マネー'),
        )
	DAY_OR_NIGHT = (
        ('日勤','日勤'),
        ('夜勤', '夜勤'),
        )
	genba = forms.Select(attrs={"class":"form-select"}),
	shift = forms.ChoiceField(label="昼夜シフト", choices=DAY_OR_NIGHT, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	distance = forms.Select(attrs={"class":"form-select", "placeholder": "距離"}),
	highway_start = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'高速道路乗ったインター'}))
	highway_end = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'高速道路降りたインター'}))
	highway_payment = forms.ChoiceField(label="支払い方法", choices=PAYMENT_TYPES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	parking = forms.Select(attrs={"class":"form-select", "placeholder": "駐車料金"}),
	hotel = forms.Select(attrs={"class":"form-select", "placeholder": "宿泊料金"}),
	other_payment = forms.BooleanField(label="その他経費", required=False),
	other_payment_amount = forms.Select(attrs={"class":"form-select", "placeholder": "金額"}),
	paid_by = forms.Select(attrs={"class":"form-select", "placeholder": "建替人"}),
	daily_details = forms.CharField(label="作業内容", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	daily_note = forms.CharField(label="その他連絡事項", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	kentaikyo = forms.BooleanField(label="建退共", required=False),
	start_time = forms.TimeField(label="作業開始時間", widget=forms.TimeInput(attrs={'type': 'time'}))
	end_time = forms.TimeField(label="作業終了時間", widget=forms.TimeInput(attrs={'type': 'time'}))
	break_time = forms.CharField(label="休憩時間", max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = DailyReport
		fields = ('genba', 'distance', 'highway_start', 'highway_end', 'highway_payment', 'shift', 'parking', 'hotel', 'other_payment', 'other_payment_amount', 'paid_by', 'daily_details', 'daily_note', 'kentaikyo', 'start_time', 'end_time', 'break_time')
		labels = {
           'genba':'現場名',
           'distance':'走行距離数',
           'parking':'駐車場利用料金（利用した場合のみ）',
           'hotel':'宿泊利用料金（利用した場合のみ）',
		   'paid_by': '建替人',
		   'other_payment': 'その他使ったもの',
		   'other_payment_amount': '使った金額', 
		   'kentaikyo':'建退共',
           }
		