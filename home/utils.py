from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.db.models import Q
from django.db.models import Count


def signup(request):
    if request.method=='POST' and 'pro_pic' in request.FILES:
        try:
            unm=request.POST['username']
            email=request.POST['email']
            pro_pic=request.FILES['pro_pic']
            password=request.POST['password']
            login=Login(username=unm,password=password,user_image=pro_pic)
            login.save()
            data=Signup(username=unm,email=email,user_image=pro_pic,password=password,login=login)
            data.save()
            # return render(request,'signup.html',{'success':'registered'})
            # return HttpResponse("success")
            return redirect('/login')
        except Exception as err:
            return HttpResponse(err)
    elif request.method=='POST':
        try:
            unm=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            pro_pic=request.POST['pro_pic']
            if pro_pic=='':
                pro_pic='user_image/download.jpg'
            login=Login(username=unm,password=password,user_image=pro_pic)
            login.save()
            data=Signup(username=unm,email=email,user_image=pro_pic,password=password,login=login)
            data.save();
            # return render(request,'signup.html',{'success':'registered'})
            # return HttpResponse("success")
            return redirect('/login')
        except Exception as err:
            return HttpResponse(err)
    else:
        return render(request,'signup.html')
       

def login(request):
    if request.method=='POST':
        try:
            un=request.POST['username']
            pw=request.POST['password']
            user=Login.objects.get(username=un,password=pw)
            print(user.id)
            # setting user session
            request.session['log_id']=user.id 
            return redirect('/recipe')
        except Exception as err:
            return HttpResponse(err)
    else:
        # return render(request, 'loguser.html')
        return render(request, 'login.html')


def createpost(request):
    if request.method=='POST':
        try:
            log_id= request.session['log_id']
            ename=request.POST['recipename']
            cname=request.POST['cat']
            print(cname)
            rimg=request.FILES['recipe_image']
            print(rimg)
            dsc=request.POST['description']
            print(cname)
            login=Login.objects.get(id=log_id)
            post=Post(name=ename,description=dsc,post_image=rimg,category=cname,login=login)
            post.save()
            return redirect('/postrecipe')
        except Exception as err:
            return HttpResponse(err)
    elif Post.objects.all():
        print("post")
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        posts=Post.objects.filter(login=id).order_by('-date')
        newpost=Post.objects.filter(login=id).order_by('-date')[:1]
        cate=Category.objects.all()
            
        if Interaction.objects.all():
            cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

                # tlk=Interaction.objects.values('post').order_by().annotate(Count('likes'))
            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                    
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)

            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)

            posts={
                    'tlk':tlk,
                    'trend':trend,
                    'lk':lk,
                    'cmt':cmt,
                    'posts':posts,
                    'user':user,
                    'cate':cate,
                    'newpost':newpost
                }
            return render(request,'createpost.html',posts)
        else:
            posts={
                    
                    'posts':posts,
                    'user':user,
                    'cate':cate,
                    'newpost':newpost
                }
            return render(request,'createpost.html',posts)

    else:
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        cate=Category.objects.all()
        posts={
            'cate':cate,
            'user':user,
        }
        return render(request,'createpost.html',posts)

def logout(request):
    try:
        del request.session['log_id']
        return redirect("/login")
    except:
        return HttpResponse("<scrip>alert('not loged in')</script")
    
def checkuser(request):
    if 'username' in request.GET:
        usernm=request.GET['username']
        print(usernm)
        check=Login.objects.filter(username=usernm).exists()
        print(check)
        return JsonResponse({
            'exists':check
        })
    if 'email' in request.GET:
        email=request.GET['email']
        check=Signup.objects.filter(email=email).exists()
        return JsonResponse({
            'exists':check
        })


def recipe(request):
    if request.method=='POST' and 'search' in request.POST:
        if Post.objects.all():
            s=request.POST['search']
            posts = Post.objects.filter(name__icontains=s)
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            cate=Category.objects.all()
            
            cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False,).order_by('-date')[:5]
            lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
            

            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
        
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)

            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)
    
            posts={
                'tlk':tlk,
                'trend':trend,

                'lk':lk,
                'cmt':cmt,
                'posts':posts,
                'user':user,
                'cat':cate,
            }
            return render(request,'grid2.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Signup.objects.get(id=id)
            posts={
                'cat':cate,
                'user':user, 
                }
            return render(request,'grid2.html',posts)


    elif request.method=='POST' and 'cat' in request.POST:
        if Post.objects.all():
            cat=request.POST['cat']
            posts = Post.objects.filter(category=cat)
            id= request.session['log_id']
            user=Signup.objects.get(id=id)
            cate=Category.objects.all()
            cmt=Interaction.objects.filter(~Q(user=id),comment__isnull=False).order_by('-date')[:5]
            lk=Interaction.objects.filter(~Q(user=id),likes__isnull=False).order_by('-date')[:3]
            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

            
            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
        
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)

            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)
    
            posts={
                'tlk':tlk,
                'trend':trend,

                'lk':lk,
                'cmt':cmt,
                'posts':posts,
                'user':user,
                'cat':cate,
            }
            
            return render(request,'grid2.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Signup.objects.get(id=id)
            posts={
                'cat':cate,
                'user':user, 
                }
            return render(request,'grid2.html',posts)


    
        
        # print(user)

        # posts=Post.objects.all()
        # print(posts)
        # cate=Category.objects.all()
        # print(cate)

    elif Post.objects.all():

        id= request.session['log_id']
        user=Login.objects.get(id=id)
        posts=Post.objects.all()
        cate=Category.objects.all()

        if Postcomment.objects.all():
            # comment notification
            ncmt=Postcomment.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            posts={
                    
                    'ncmt':ncmt,
                    # 'trend':trend,
                    # 'trend':trend,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }

        elif Postlike.objects.all():
            # like notification
            nlk=Postlike.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
            lk=Postlike.objects.values('post').order_by().annotate(Count('likes'))[:1]
            vv = t.values("likes")
            tlk=Post.objects.get(id=vv)
            posts={
                    'nlk':nlk,
                    'tlk':tlk,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }

        elif Postcomment.objects.all() and Postcomment.objects.all():
            nlk=Postlike.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
            lk=Postlike.objects.values('post').order_by().annotate(Count('likes'))[:1]
            vv = t.values("likes")
            tlk=Post.objects.get(id=vv)
            ncmt=Postcomment.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            posts={
                    
                    'ncmt':ncmt,
                    'nlk':nlk,
                    'tlk':tlk,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }
        
        return render(request,'grid2.html',posts)





        if Interaction.objects.all():
            # trending posts
            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)
            print(trend)
            if Interaction.objects.filter(comment__isnull=False):
                
                # comment notification
                ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
                posts={
                    
                    'ncmt':ncmt,
                    # 'trend':trend,
                    'trend':trend,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }


            if Interaction.objects.filter(likes__isnull=False):
                print("like===================")
                # most liked post
                lk=Interaction.objects.values('post').order_by().annotate(Count('likes'))[:1]
                vv = t.values("likes")
                tlk=Post.objects.get(id=vv)
                print(lk)

                # like notification
                nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
                posts={
                    'tlk':tlk,
                    'nlk':nlk,
                    'trend':trend,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }
           


           
            posts={
                # 'tlk':tlk,
                # 'nlk':nlk,
                # 'ncmt':ncmt,
                'trend':trend,

                'posts':posts,
                'cat':cate,
                'user':user, 
                }
            
            return render(request,'grid2.html',posts)


        else:
            posts={
                'posts':posts,
                'cat':cate,
                'user':user, 
                }
            
            return render(request,'grid2.html',posts)

        # if Interaction.objects.all():
        #     post_id=Post.objects.all()
            # print(post_id)

            # for i in post_id:
                # print(i.id)
                # v=Interaction.objects.filter(post=i.id,user=user)
                # for v in v:
                #     print(v.id)
                #     print(v.comment)
                    # print(v.likes)
                    # if Interaction.objects.filter(comment__isnull=False):
                    #     lk=Interaction.objects.filter(post=i.id,likes__isnull=False).count()[:1]
                    #     print(lk)


                # if v.comment =='' and v.likes=='':
                #     print("null")
            # v=Interaction.objects.filter(comment__isnull=False)
            # print(v)
            # v=Interaction.objects.filter()
            # print(v)
            # if Interaction.objects.filter(likes__isnull=False):
            #     print("like==================recipe")
            #     user_id= request.session['log_id']
                # post_id=Post.objects.get(id=id)

                # user=Login.objects.get(id=user_id)
                # print("like==================recipe")
                # lk=Interaction.objects.filter(post=post_id,likes__isnull=False).count()[:1]
                # print("lk")
                # print(lk)
                # nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
                # print(nlk)
                # tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=0)[:1]
                # print(tlk)
                # lks = tlk.values("post_id")
                # tlk=Post.objects.get(id=lks)
                # posts={
                            # 'ncmt':ncmt,
                            # 'nlk':nlk,
                            # 'tlk':tlk,
                            # 'trend':trend,

                            # 'lk':lk,
                            # 'cmt':cmt,
            #                 'posts':posts,
            #                 'user':user,
            #                 'cat':cate,
            #     }
                        
            #     return render(request,'grid2.html',posts)

            # elif Interaction.objects.filter(comment__isnull=False): 
            #     print("comment===============")
            #     cmt=Interaction.objects.filter(comment__isnull=False,post=post_id).order_by('-date')
                # ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
                # t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
                # vv = t.values("post_id")
                # trend=Post.objects.get(id=vv)

                # posts={
                #         'ncmt':ncmt,
                        # 'nlk':nlk,
                        # 'tlk':tlk,
                        # 'trend':trend,

                        # 'lk':lk,
                #         'cmt':cmt,
                #         'posts':posts,
                #         'user':user,
                #         'cat':cate,
                # }
                    
                # return render(request,'grid2.html',posts)

            # elif Interaction.objects.filter(post=post_id,comment__isnull=False,likes__isnull=False):
            # else:
            #     print("both==============")
                # likes
                # lk=Interaction.objects.filter(post=post_id,likes__isnull=False).count()
                # nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
                # tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                # lks = tlk.values("post_id")
                # tlk=Post.objects.get(id=lks)
                # comments
                # cmt=Interaction.objects.filter(comment__isnull=False,post=posts).order_by('-date')
                # ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
                # t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
                # vv = t.values("post_id")
                # trend=Post.objects.get(id=vv)

                # posts={
                #         'ncmt':ncmt,
                #         'nlk':nlk,
                #         'tlk':tlk,
                #         'trend':trend,

                #         'lk':lk,
                #         'cmt':cmt,
                #         'posts':posts,
                #         'user':user,
                #         'cat':cate,
                # }
                    
                # return render(request,'grid2.html',posts)
        # else:
        #     posts={
        #                 'posts':posts,
        #                 'user':user,
        #                 'cat':cate,
        #         }
                    
        #     return render(request,'grid2.html',posts)

                
                # cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]

                # lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

                # t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
                
                # if Interaction.objects.filter(likes__isnull=False):
                #     tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                    
                #     lks = tlk.values("post_id")
                #     tlk=Post.objects.get(id=lks)
                #     vv = t.values("post_id")
                #     trend=Post.objects.get(id=vv)

                #     posts={
                #         'tlk':tlk,
                #         'trend':trend,
                #         'lk':lk,
                #         'cmt':cmt,
                #         'posts':posts,
                #         'user':user,
                #         'cat':cate,
                #     }
                    
                #     return render(request,'grid2.html',posts)

                

                # vv = t.values("post_id")
                # trend=Post.objects.get(id=vv)

                # posts={
                #     # 'tlk':tlk,
                #     'trend':trend,
                #     'lk':lk,
                #     'cmt':cmt,
                #     'posts':posts,
                #     'user':user,
                #     'cat':cate,
                # }
                
                # return render(request,'grid2.html',posts)

        # else:
        #         cate=Category.objects.all()
        #         id= request.session['log_id']
        #         user=Signup.objects.get(id=id)
                # posts=Post.objects.all()
                # posts={
                #     'posts':posts,
                #     'cat':cate,
                #     'user':user, 
                #     }
                # return render(request,'grid2.html',posts)

    else:
        cate=Category.objects.all()
        id= request.session['log_id']
        user=Signup.objects.get(id=id)
        posts={
            'cat':cate,
            'user':user, 
            }
        return render(request,'grid2.html',posts)
            
    # except Exception as err:
    #     print(err)

def userprofile(request):
    id= request.session['log_id']
    user=Login.objects.get(id=id)
    if Post.objects.all():
        posts=Post.objects.filter(login=id)
        cate=Category.objects.all()
        if Interaction.objects.all():
            cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

            
            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)

            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)

            posts={
                'tlk':tlk,
                'trend':trend,
                'lk':lk,
                'cmt':cmt,
                'posts':posts,
                'user':user,
                'cat':cate,
            }
            return render(request,'account.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Signup.objects.get(id=id)
            posts=Post.objects.all()
            posts={
                'posts':posts,
                'cat':cate,
                'user':user, 
                }
            return render(request,'account.html',posts)
    else:
        posts={
                'user':user, 
               }
        return render(request,'account.html',posts)    

def updatepost(request,id):
    if Post.objects.all():
        if request.method=='POST' and 'recipe_image' in request.FILES:
            try:
                # log_id= request.session['log_id']
                ename=request.POST['recipename']
                cname=request.POST['cat']
                print(cname)
                rimg=request.FILES['recipe_image']
                print(rimg)

                dsc=request.POST['description']
                print(cname)

                # login=Login.objects.get(id=log_id)
                post=Post.objects.get(id=id)

                post.name=ename
                post.description=dsc
                post.post_image=rimg
                post.category=cname
                
                # post=Post(name=ename,description=dsc,post_image=rimg,category=cname,login=login)
                post.save()
                # return redirect('/postrecipe')
                return redirect('/userprofile')
            except Exception as err:
                return HttpResponse(err)

        elif request.method=='POST':
            try:
                # log_id= request.session['log_id']
                ename=request.POST['recipename']
                cname=request.POST['cat']
                print(cname)
                # rimg=request.FILES['recipe_image']
                # print(rimg)

                dsc=request.POST['description']
                print(cname)

                # login=Login.objects.get(id=log_id)
                post=Post.objects.get(id=id)

                post.name=ename
                post.description=dsc
                post.post_image=post.post_image
                post.category=cname
                
            
                post.save()
                
                return redirect('/userprofile')
            except Exception as err:
                return HttpResponse(err)


        user_id= request.session['log_id']
        user=Login.objects.get(id=user_id)

        posts=Post.objects.get(id=id)
        print(posts.post_image)

        cate=Category.objects.all()
        
        if Interaction.objects.all():
            cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

            # tlk=Interaction.objects.values('post').order_by().annotate(Count('likes'))
            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)

            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)

            posts={
                'tlk':tlk,
                'trend':trend,
                'lk':lk,
                'cmt':cmt,

                'posts':posts,
                'user':user,
                'cate':cate,
            }
            return render(request,'updatepost.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Signup.objects.get(id=id)
            posts={
                'posts':posts,
                'cate':cate,
                'user':user, 
                }
            return render(request,'updatepost.html',posts)
    else:
        
        posts={
                'user':user, 
               }
        return render(request,'updatepost.html',posts) 

def deletepost(request,id):
    Post.objects.get(id=id).delete()
    return redirect('/userprofile')

# update profile
def updateprofile(request): 
    if request.method=='POST' and 'user_image' in request.FILES:
        try:
            log_id= request.session['log_id']
            unm=request.POST['username']
            email=request.POST['email']
            u_img=request.FILES['user_image']
            user=Login.objects.get(id=log_id)
            log_user=Signup.objects.get(id=log_id)
            log_user.username=unm
            log_user.user_image=u_img
            log_user.save()

            user.username=unm
            user.email=email
            user.user_image=u_img
            user.save()
                
            # return redirect('/updateprofile')
            posts={
                'seml':log_user,
                'user':user, 
                }
            return render(request,'updateprofile.html',posts) 
        except Exception as err:
            return HttpResponse(err)

    elif request.method=='POST':
        try:
            log_id= request.session['log_id']
            unm=request.POST['username']
            email=request.POST['email']
            user=Signup.objects.get(id=log_id)
            user.username=unm
            user.email=email
            user.save()
            log_user=Signup.objects.get(id=log_id)
            log_user.username=unm
            log_user.save()
            # return redirect('/updateprofile')
            posts={
                'seml':log_user,
                'user':user, 
                }
            return render(request,'updateprofile.html',posts) 
                
        except Exception as err:
            return HttpResponse(err)
    elif Interaction.objects.all():
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        seml=Signup.objects.get(id=id)
        posts=Post.objects.filter(login=id)
        cate=Category.objects.all()

        cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
        lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

        t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

         
        tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                
        lks = tlk.values("post_id")
        tlk=Post.objects.get(id=lks)

        vv = t.values("post_id")
        trend=Post.objects.get(id=vv)

        posts={
                'tlk':tlk,
                'trend':trend,
                'lk':lk,
                'cmt':cmt,
                'seml':log_user,
                'posts':posts,
                'user':user,
                'cat':cate,
                'seml':seml
        }
        
        return render(request,'updateprofile.html',posts)
        
    else:
        
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        log_user=Signup.objects.get(login=user)
        posts={
                'seml':log_user,
                'user':user, 
               }
        return render(request,'updateprofile.html',posts) 

        # id= request.session['log_id']
        # user=Login.objects.get(id=id)
        # seml=Signup.objects.get(id=id)
        # posts=Post.objects.filter(login=id)
        # cate=Category.objects.all()
        # if Post.objects.all():
        #     cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
        #     lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

        #     t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

         
        #     tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                
            # lks = tlk.values("post_id")
            # tlk=Post.objects.get(id=lks)

            # vv = t.values("post_id")
            # trend=Post.objects.get(id=vv)

            # posts={
            #     'tlk':tlk,
            #     'trend':trend,
            #     'lk':lk,
            #     'cmt':cmt,
            #     'seml':log_user,
            #     'posts':posts,
            #     'user':user,
            #     'cat':cate,
            #     'seml':seml
            # }
        
        #     return render(request,'updateprofile.html',posts)
        # else:
        #     cate=Category.objects.all()
        #     id= request.session['log_id']
        #     user=Signup.objects.get(id=id)
        #     posts={
        #         'posts':posts,
        #         'cate':cate,
        #         'user':user, 
        #         'seml':seml,
        #         }
        #     return render(request,'updateprofile.html',posts)
    # else:
    #     id= request.session['log_id']
    #     user=Login.objects.get(id=id)
    #     log_user=Signup.objects.get(login=user)
    #     posts={
    #             'seml':log_user,
    #             'user':user, 
    #            }
    #     return render(request,'updateprofile.html',posts) 

def interactions(request,id):
    if request.method=='POST' and 'comment' in request.POST:
        print("coment==================")
        comment=request.POST['comment']
        user_id= request.session['log_id']
        post_id=Post.objects.get(id=id)
        cu=Login.objects.get(id=user_id)
        comment=Postcomment(comment=comment,user=cu,post=post_id)
        comment.save()
        # errrro------------------
        if Interaction.objects.all():
            print("interaction")
            inte=Interaction.objects.filter(comment__isnull=False,likes__isnull=False,post=id).order_by('-date')
            user=Login.objects.get(id=user_id)
            posts=Post.objects.get(id=id)
            cate=Category.objects.all()
            lk=Interaction.objects.filter(post=posts,likes__isnull=False).count()

            ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
            
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)

            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)

            posts={
                'ncmt':ncmt,
                'nlk':nlk,
                'tlk':tlk,
                'trend':trend,

                'lk':lk,
                'cmt':inte,
                'posts':posts,
                'user':user,
                'cat':cate,
            }
            return render(request,'interactions.html',posts)
        else:
            
            posts={
                
                'cmt':inte,
                'posts':posts,
                'user':user,
                'cat':cate,
            }
            return render(request,'interactions.html',posts)


    elif request.method=='POST' and 'like' in request.POST:
        print("like====================like")
        likes=request.POST['like']
        user_id= request.session['log_id']
        posts=Post.objects.get(id=id)
        user=Login.objects.get(id=user_id)
        # ck=Interaction.objects.filter(post=post_id,user=cu)
        # print(ck)
        print("like====================1")
        l=Interaction.objects.filter(~Q(user=posts.login),post=posts,likes__isnull=True)
        print(l,'null')
        print(posts.login)

        if Interaction.objects.filter(~Q(user=posts.login),post=posts,likes__isnull=True):
            print("like====================2")
            likes= Interaction(likes=likes,user=user,post=posts)
            likes.save()

            # if Interaction.objects.filter(likes__isnull=False):
            #     lk=Interaction.objects.filter(post=posts,likes__isnull=False).count()
            #     nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
            #     tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
            #     lks = tlk.values("post_id")
            #     tlk=Post.objects.get(id=lks)
            #     posts={
                        # 'ncmt':ncmt,
                        # 'nlk':nlk,
                        # 'tlk':tlk,
                        # 'trend':trend,

                        # 'lk':lk,
                        # 'cmt':cmt,
                        # 'posts':posts,
                        # 'user':user,
                        # 'cat':cate,
                # }
                    
            #     return render(request,'interactions.html',posts)

            # elif Interaction.objects.filter(comment__isnull=False): 
            #     cmt=Interaction.objects.filter(comment__isnull=False,post=posts).order_by('-date')
            #     ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            #     t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
            #     vv = t.values("post_id")
            #     trend=Post.objects.get(id=vv)

                # posts={
                #         'ncmt':ncmt,
                        # 'nlk':nlk,
                        # 'tlk':tlk,
                        # 'trend':trend,

                        # 'lk':lk,
                #         'cmt':cmt,
                #         'posts':posts,
                #         'user':user,
                #         'cat':cate,
                # }
                    
                # return render(request,'interactions.html',posts)

        elif Interaction.objects.filter(post=posts,user=user,likes__isnull=False):
            print("false")
            user_id= request.session['log_id']
            posts=Post.objects.get(id=id)
            user=Login.objects.get(id=user_id)
            if Interaction.objects.filter(likes__isnull=False):
                lk=Interaction.objects.filter(post=posts,likes__isnull=False).count()
                nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
                tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                lks = tlk.values("post_id")
                tlk=Post.objects.get(id=lks)
                posts={
                        # 'ncmt':ncmt,
                        'nlk':nlk,
                        'tlk':tlk,
                        # 'trend':trend,

                        'lk':lk,
                        # 'cmt':cmt,
                        'posts':posts,
                        'user':user,
                        'cat':cate,
                }
                    
                return render(request,'interactions.html',posts)

            elif Interaction.objects.filter(comment__isnull=False): 
                cmt=Interaction.objects.filter(comment__isnull=False,post=posts).order_by('-date')
                ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
                t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
                vv = t.values("post_id")
                trend=Post.objects.get(id=vv)

                posts={
                        'ncmt':ncmt,
                        # 'nlk':nlk,
                        # 'tlk':tlk,
                        'trend':trend,

                        # 'lk':lk,
                        'cmt':cmt,
                        'posts':posts,
                        'user':user,
                        'cat':cate,
                }
                    
                return render(request,'interactions.html',posts)

            elif Interaction.objects.filter(comment__isnull=False,likes__isnull=False):
                # likes
                lk=Interaction.objects.filter(post=posts,likes__isnull=False).count()
                nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
                tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                lks = tlk.values("post_id")
                tlk=Post.objects.get(id=lks)
                # comments
                cmt=Interaction.objects.filter(comment__isnull=False,post=posts).order_by('-date')
                ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
                t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
                vv = t.values("post_id")
                trend=Post.objects.get(id=vv)

                posts={
                        'ncmt':ncmt,
                        'nlk':nlk,
                        'tlk':tlk,
                        'trend':trend,

                        'lk':lk,
                        'cmt':cmt,
                        'posts':posts,
                        'user':user,
                        'cat':cate,
                }
                    
                return render(request,'interactions.html',posts)
    
        # else:
        
           

            # user=Login.objects.get(id=user_id)
            # posts=Post.objects.get(id=id)
            # cate=Category.objects.all()

            # cmt=Interaction.objects.filter(comment__isnull=False,likes__isnull=False,post=posts).order_by('-date')
            # lk=Interaction.objects.filter(post=posts,likes__isnull=False).count()

            # ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            # nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

            # t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
            # tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
            
            # lks = tlk.values("post_id")
            # tlk=Post.objects.get(id=lks)

            # vv = t.values("post_id")
            # trend=Post.objects.get(id=vv)

            # posts={
            #     'ncmt':ncmt,
            #     'nlk':nlk,
            #     'tlk':tlk,
            #     'trend':trend,

            #     'lk':lk,
            #     'cmt':cmt,
            #     'posts':posts,
            #     'user':user,
            #     'cat':cate,
            # }
            # return render(request,'interactions.html',posts)


    elif Interaction.objects.all():
        print("interaction============================")   

        user_id= request.session['log_id']
        user=Login.objects.get(id=user_id)
        posts=Post.objects.get(id=id)
        cate=Category.objects.all()
        # cmt=Interaction.objects.filter(post=id)
        if Interaction.objects.filter(likes__isnull=False):
            print("like======================")
            lk=Interaction.objects.filter(post=posts,likes__isnull=False).count()
            print(lk)
            nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
            print(nlk)

            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=0)[:1]
            print(tlk)
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)

            posts={
                    # 'ncmt':ncmt,
                    'nlk':nlk,
                    'tlk':tlk,
                    # 'trend':trend,

                    'lk':lk,
                    # 'cmt':cmt,
                    'posts':posts,
                    'user':user,
                    'cat':cate,
            }
                
            return render(request,'interactions.html',posts)

        elif Interaction.objects.filter(comment__isnull=False): 
            print("comment===================")
            cmt=Interaction.objects.filter(comment__isnull=False,post=posts).order_by('-date')
            ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)

            posts={
                    'ncmt':ncmt,
                    # 'nlk':nlk,
                    # 'tlk':tlk,
                    'trend':trend,

                    # 'lk':lk,
                    'cmt':cmt,
                    'posts':posts,
                    'user':user,
                    'cat':cate,
            }
                
            return render(request,'interactions.html',posts)

        elif Interaction.objects.filter(comment__isnull=False,likes__isnull=False):
            print("both==================")
            # likes
            lk=Interaction.objects.filter(post=posts,likes__isnull=False).count()
            nlk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]
            tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
            lks = tlk.values("post_id")
            tlk=Post.objects.get(id=lks)
            # comments
            cmt=Interaction.objects.filter(comment__isnull=False,post=posts).order_by('-date')
            ncmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
            t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]
            vv = t.values("post_id")
            trend=Post.objects.get(id=vv)

            posts={
                    'ncmt':ncmt,
                    'nlk':nlk,
                    'tlk':tlk,
                    'trend':trend,

                    'lk':lk,
                    'cmt':cmt,
                    'posts':posts,
                    'user':user,
                    'cat':cate,
            }
                
            return render(request,'interactions.html',posts) 


    else:
        print("else =======================")
        user_id= request.session['log_id']
        user=Login.objects.get(id=user_id)
        posts=Post.objects.get(id=id)
        # cate=Category.objects.all()
        posts={
            'user':user,
            'posts':posts,
        }
        return render(request,'interactions.html',posts)

def notification(request):
    if Interaction.objects.all():
        id= request.session['log_id']
        user=Login.objects.get(id=id)

        posts=Post.objects.filter(login=id)
        cate=Category.objects.all()

        cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')
        lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')

        t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

        
        # tlk=Interaction.objects.values('post').order_by().annotate(Count('likes'))
        tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
        
        
        lks = tlk.values("post_id")
        tlk=Post.objects.get(id=lks)

    

        vv = t.values("post_id")
        trend=Post.objects.get(id=vv)
    
        posts={
            'tlk':tlk,
            'trend':trend,
            'lk':lk,
            'cmt':cmt,
            'posts':posts,
            'user':user,
            'cat':cate,
        }
        return render(request,'notification.html',posts)
    else:
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        posts={
                'user':user, 
            }
        return render(request,'notification.html',posts)


    
 







    
