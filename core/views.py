from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, BillingAddress, Payment
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
	"""Оформление заказа"""
	def get(self, *args, **kwargs):
		form = CheckoutForm()
		order = Order.objects.get(user=self.request.user, ordered=False)
		context = {
			'form':form,
			'order':order
		}
		return render(self.request, 'checkout.html', context)
	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		if self.request.POST.get('payment_option') == 'C':
			try:
				order = Order.objects.get(user=self.request.user, ordered=False)
				if form.is_valid():
					city = form.cleaned_data.get('city')
					street_address = form.cleaned_data.get('street_address')
					zip = form.cleaned_data.get('zip')
					name = form.cleaned_data.get('name')
					phone = form.cleaned_data.get('phone')
					# save_billing_address = form.cleaned_data.get('save_billing_address')
					# save_info = form.cleaned_data.get('save_info')
					payment_option = form.cleaned_data.get('payment_option')
					try:
						billing_address = BillingAddress.objects.get(user=self.request.user)
					except:
						billing_address = BillingAddress(
							user=self.request.user,
							city=city,
							street_address=street_address,
							zip=zip,
							name=name,
							phone=phone,
						)
					billing_address.save()
					order.billing_address = billing_address
					order.ordered = True
					order.save()
					messages.warning(self.request, 'Filed checkout!')
					return redirect('/')
			except ObjectDoesNotExist:
				messages.error(self.request, 'У вас еще нет товаров в корзине')
				return redirect('core:order-summary')
		else:
			messages.warning(self.request, 'Яндекс касса еще не привязана к сайту!')
			return redirect('core:checkout')


class PaymentView(View):
	def get(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		context = {
			'order':order,
		}
		return render(self.request, 'payment.html', context)

	def post(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		token = self.request.POST.get('stripeToken')
		amount = int(order.get_total() * 100)
		try:
			charge = stripe.Charge.create(
				amount=amount,
				currency="usd",
				source=token
			)
			# create the payment
			payment = Payment()
			payment.stripe_charge_id = charge['id']
			payment.user = self.request.user
			payment.amount = order.get_total()
			payment.save()

			# assign the payment to the order

			order.ordered = True
			order.payment = payment
			order.save()

			messages.success(self.request, 'Your order was succsessfull')
			return redirect('/')

		except stripe.error.CardError as e:
			body = e.json_body
			err = body.get('error', {})
			messages.warning(self.request, f"{err.get('message')}")
			return redirect("/")

		except stripe.error.RateLimitError as e:
			# Too many requests made to the API too quickly
			messages.warning(self.request, "Rate limit error")
			return redirect("/")

		except stripe.error.InvalidRequestError as e:
			# Invalid parameters were supplied to Stripe's API
			print(e)
			messages.warning(self.request, "Invalid parameters")
			return redirect("/")

		except stripe.error.AuthenticationError as e:
			# Authentication with Stripe's API failed
			# (maybe you changed API keys recently)
			messages.warning(self.request, "Not authenticated")
			return redirect("/")

		except stripe.error.APIConnectionError as e:
			# Network communication with Stripe failed
			messages.warning(self.request, "Network error")
			return redirect("/")

		except stripe.error.StripeError as e:
			# Display a very generic error to the user, and maybe send
			# yourself an email
			messages.warning(
				self.request, "Something went wrong. You were not charged. Please try again.")
			return redirect("/")

		except Exception as e:
			# send an email to ourselves
			messages.warning(
				self.request, "A serious error occurred. We have been notifed.")
			return redirect("/")









class HomeView(ListView):
	"""Домашная страница"""
	model = Item
	paginate_by = 10
	template_name = 'home.html'


class OrderSummaryView(LoginRequiredMixin, View):
	"""Отображение корзины с товарами"""
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context = {
				'object':order
			}
			return render(self.request, 'order_summary.html', context)
		except ObjectDoesNotExist:
			messages.error(self.request, 'У вас еще нет товаров в корзине')
			return redirect('/')





class ItemDetailView(DetailView):
	model = Item
	template_name = 'product.html'

@login_required
def add_to_cart(request, slug):
	"""Добавить в корзину"""
	item = get_object_or_404(Item, slug=slug)
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False

	                                             )
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#Проверяем есть ли продукт в заказе
		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, 'Количество обновлено!')
		else:
			messages.info(request, 'This item was added to your cart')
			order.items.add(order_item)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request, 'This item was added to your cart')
	return redirect('core:order-summary')

@login_required
def remove_from_cart(request, slug):
	"""Удалить товар из корзины"""
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# Проверяем есть ли продукт в заказе
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]
			order.items.remove(order_item)
			messages.info(request, 'Товар удален из корзины!')
			return redirect('core:order-summary')
		else:
			#Сообщение о том что заказ не включает этот продукт
			messages.info(request, 'This item was not in your cart')
			return redirect('core:order-summary')
	else:
		#Добавляем сообщение о том, что у пользователя нет заказа
		messages.info(request, 'You dont have an active order')
		return redirect('core:product', slug=slug)
	return redirect('core:product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
	"""Удалить товар из количества"""
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# Проверяем есть ли продукт в заказе
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]
			if order_item.quantity >1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
			messages.info(request, 'Количество товара уменьшено')
			return redirect('core:order-summary')
		else:
			#Сообщение о том что заказ не включает этот продукт
			messages.info(request, 'This item was not in your cart')
			return redirect('core:order-summary')
	else:
		#Добавляем сообщение о том, что у пользователя нет заказа
		messages.info(request, 'You dont have an active order')
		return redirect('core:order-summary')
	return redirect('core:order-summary', slug=slug)