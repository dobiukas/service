from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import path
from .models import Car, Service, Order, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.forms import User
from django.views.generic.edit import FormMixin
from .forms import OrderCommentForm, UserUpdateForm, ProfilisUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

def index(request):
    paslaugu_kiekis = Service.objects.count()
    atliktu_uzsakymu_kiekis = Order.objects.filter(status__exact='a').count()
    automobiliu_kiekis = Car.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'atliktu_uzsakymu_kiekis': atliktu_uzsakymu_kiekis,
        'automobiliu_kiekis': automobiliu_kiekis,
        'num_visits': num_visits,
    }

    # renderiname base.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)


def cars(request):
    paginator = Paginator(Car.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars': paged_cars
    }
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})



class OrderListView(generic.ListView):
    model = Order
    template_name = 'orders.html'
    paginate_by = 5

class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('due_date')


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order.html'
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    # įtraukiame formą į kontekstą, inicijuojame pradinę 'book' reikšmę.
    # def get_context_data(self, *args, **kwargs):
    #     context = super(OrderDetailView, self).get_context_data(**kwargs)
    #     context['form'] = OrderCommentForm(initial={'order': self.object})
    #     return context

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.user = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)

class OrderByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = ['car', 'due_date']
    success_url = "/autoservice/user_order/"
    template_name = 'user_order_form.html'

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class OrderLineByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = OrderLine
    fields = ['service', 'qty']
    template_name = 'userline_form.html'

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)


class OrderByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    fields = ['car', 'due_date']
    template_name = 'user_order_form.html'

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user


class OrderByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    success_url = "/autoservice/user_order/"
    template_name = 'user_order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(owner__icontains=query) | Q(licence_plate__icontains=query) | Q(vin_code__icontains=query) | Q(car_model__manufacturer__icontains=query) | Q(car_model__model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')





@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)