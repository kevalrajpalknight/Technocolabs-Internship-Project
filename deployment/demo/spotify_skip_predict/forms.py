from django import forms

CONTEXT_TYPE = (
    ('editorial_playlist','Editorial Playlist'),
    ('user_collection', 'User Collection'),
    ('radio','Radio'),
    ('catalog', 'Catalog'),
    ('charts', 'Charts'),
)
HIST_USER_BEHAVIOR_REASON_START = (
    ('trackdone', 'Trackdone'),
    ('fwdbtn', 'Forward Button'),
    ('backbtn', 'Backward Button'),
    ('clickrow', 'Click Row'),
    ('appload', 'Appload'),
    ('playbtn', 'Play Button'),
    ('remote', 'Remote'),
    ('trackerror', 'Track Error'),
    ('endplay', 'End Play'),
)

HIST_USER_BEHAVIOR_REASON_END = (
    ('trackdone', 'Trackdone'),
    ('fwdbtn', 'Forward Button'),
    ('backbtn', 'Backward Button'),
    ('clickrow', 'Click Row'),
    ('logout', 'Logout'),
    ('remote', 'Remote'),
    ('endplay', 'End Play'),
)

PREMIUM = (
    (True, 'Premium'),
    (False, 'Non-Premium'),
)

MODE = (
    ('minor', 'Minor'),
    ('major', 'Major'),
)




class UserInputForm(forms.Form):
    session_length = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "session_lenght",
        }

    ))
    context_type = forms.ChoiceField(widget=forms.Select(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "context_type",
        }
    ), choices=CONTEXT_TYPE)

    hist_user_behavior_reason_start = forms.ChoiceField(widget=forms.Select(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "hist_user_behavior_reason_start",
        }
    ), choices=HIST_USER_BEHAVIOR_REASON_START)

    hist_user_behavior_reason_end = forms.ChoiceField(widget=forms.Select(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "hist_user_behavior_reason_end",
        }
    ), choices=HIST_USER_BEHAVIOR_REASON_END)

    mode = forms.ChoiceField(widget=forms.Select(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "mode",
        }
    ), choices=MODE)
    premium = forms.ChoiceField(widget=forms.Select(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "premium",
        }
    ), choices=PREMIUM)