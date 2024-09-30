from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect

from django.urls import reverse,reverse_lazy

from django.views.generic import View,TemplateView,UpdateView,CreateView,DetailView

from store.forms import SignUpForm,LoginForm,UserProfileForm,ProjectForm

from django.contrib.auth import authenticate,login

from store.models import UserProfile,Project,WishListItems,OrderSummary

KEY_SECRET="4xkXtLOnixzKTIf3ae0c4RpQ"

KEY_ID="rzp_test_3So3s6SMOCVWlE"

# Create your views here.

class SignUPView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"store/register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("login")
        else:
            return render(request,"store/register.html",{"form":form_instance})






class LoginView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"store/login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            user_object=authenticate(request,**data)

            if user_object:

                login(request,user_object)

                return redirect("index")
            
        return render (request,"store/login.html",{"form":form_instance})  

class IndexView(View):

    template_name="store/index.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.all().exclude(owner=request.user)

        return render(request,self.template_name,{"projects":qs})


class UserProfileUpdateView(UpdateView):

    model=UserProfile

    form_class=UserProfileForm

    template_name="store/profile_edit.html"

    # def get_success_url(self):

    #     return reverse("index")
    
    success_url=reverse_lazy("index")
    

 
class ProjectCreatView(CreateView):

    model=Project

    form_class=ProjectForm

    template_name="store/project_add.html"

    success_url=reverse_lazy("index")

    def form_valid(self, form):

        form.instance.owner=self.request.user

        return super().form_valid(form)
    
class MyProjectListView(View):

    def get(self,request,*args,**kwargs):

        # qs=Project.objects.filter(owner=request.user)

        qs=request.user.projects.all()

        return render(request,"store/myprojects.html",{"works":qs})





class WorksDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Project.objects.get(id=id).delete()

        return redirect("myworks")



class ProjectDetailView(DetailView):

   template_name="store/project_detail.html"

   context_object_name="project"

   model=Project



class AddToWishListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_obj=Project.objects.get(id=id)

        WishListItems.objects.create(
            wishlist_object=request.user.basket,
            project_object=project_obj
        )
        print("item has been added to whishlist")

        return redirect("index")
    
from django.db.models import Sum

class MyCartView(View):

    def get(sellf,request,*args,**kwargs):

        qs=request.user.basket.basket_items.filter(is_order_placed=False)

        total=request.user.basket.wishlist_total

        return render(request,"store/whishlist_summary.html",{"cart_items":qs,"total":total})
    
class WhishListItemRemoveView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        WishListItems.objects.get(id=id).delete()

        return redirect("whishlist-summary")  


    
import razorpay

class CheckOutView(View):

    def get(self,request,*args,**kwargs):

        client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        amount=request.user.basket.wishlist_total * 100

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

        order_summary_obj=OrderSummary.objects.create(

            user_object=request.user,
            order_id=payment.get('id')
        )

        for p in cart_items.values('project_object'):

            order_summary_obj.project_objects.add(p.get('id'))

        for ci in cart_items:
            ci.is_order_placed=True
            ci.save()

        order_summary_obj.save()


        context={
            "key":KEY_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id")
        }

        return render(request,"store/payment.html",context)
    


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name='dispatch')
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        return render(request,'store/success.html')


