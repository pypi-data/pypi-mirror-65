# django-talar

Django app for [Talar.app](https://talar.app) service.

## Installation

1. `pip install django-talar`.
2. Add `talar` to your django settings `INSTALLED_APPS`.
3. Modify code below and also insert it into django settings:

    ```python
        TALAR = {
            'project_id': env.str('TALAR_PROJECT_ID', None),
            'access_key_id': env.str('TALAR_ACCESS_KEY_ID', None),
            'access_key': env.str('TALAR_ACCESS_KEY', None),
        }
    ```

4. Include this into your core urls:

    ```python
        path('talar/', include(('talar.urls', 'talar'))),
    ```

## Basic usage

django-talar contains basic form `talar.forms.PaymentForm` and template
`talar/talar_make_payment.html` for making payments. It is suggested to
use it by adding your own view like so:

```python
def make_payment(request):
    data = {
        'external_id': EXTERNAL_ID, # You order/payment unique key that will be used to identify payment
        'amount': AMOUNT, # your data
        'currency': CURRENCY, # your data
        'continue_url': CONTINUE_URL, # Insert address for redirection after successfull payment
    }

    talar = Talar()
    url = talar.url
    data = talar.create_payment_data(data)

    payment_form = PaymentForm(data={
        'key_id': talar.access_key_id,
        'encrypted': data
    })

    return render(request, 'talar/make_payment.html', {
        'url': url,
        'payment_form': payment_form
    })
```

html code will handle redirection if everything is correct:

```html
    <div>
        <p>{% trans 'After continuing you will be redirected to payment provider site.' %}</p>
        <form action="{{ url }}" method="post" class="form-inline">
            {{ payment_form.as_p }}
            <button type=submit class="btn btn-primary">{% trans 'Pay' %}</button>
        </form>
    </div>
```
