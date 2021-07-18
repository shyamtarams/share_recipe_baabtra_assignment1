from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
from django.db.models import Q,F
from django.db.models import Count
# from django.contrib.auth.decorators import login_required


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
    log_id= request.session['log_id']
    login=Login.objects.get(id=log_id)
    if request.method=='POST' and 'search' in request.POST:
        s=request.POST['search']
        return redirect('/postrecipe')
                

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
            access=request.POST['access']
            print("acccccccess",access)
            post=Post(name=ename,description=dsc,post_image=rimg,category=cname,login=login,access=access)
            post.save()
            
            # if Follow.objects.filter(user=login):
            #     newpost=Post.objects.filter(login=id).order_by('-date')[:1]
            #     fu=Follow.objects.filter(user=login)
            #     fu.post=newpost
            #     fu.save
            # else:
            #     pass

            return redirect('/postrecipe')
        except Exception as err:
            return HttpResponse(err)

    elif Post.objects.all():
        print("===============-")
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        if Follow.objects.filter(following=user):
                print("===============--")
                ps=Post.objects.filter(login=user,access='public').order_by("-date")[:1]
                print(ps,"===-=============new")
                if ps:
                    for i in ps:
                        pn=i.id
                    # print(pn)
                    # print(id)
                    if Post.objects.filter(login=user,access='public').order_by("-date")[:1]:
    
                        fnewpost=Post.objects.get(id=pn)
                        print(fnewpost)
                        fu=Follow.objects.filter(following=user)
                        print(fu,"=====f")
                        for i in fu:
                            print(i.user)

                            
                            i.user=i.user
                            i.following=i.following
                            i.post=fnewpost
                            i.save()
                    else:
                        pass
                else:
                    pass
        else:
            pass
        print("post")
        
        posts=Post.objects.filter(login=id).order_by('-date')
        newpost=Post.objects.filter(login=id).order_by('-date')[:1]
        if newpost:
            newpost:newpost
        else:
            newpost=''
        
        


        
        # fu=Follow.objects.filter(user=user)

        cate=Category.objects.all()

        if Postcomment.objects.all() or Postlike.objects.all():
            # aposts=Post.objects.all()
            # for i in aposts:
            #     print(i.id)
            #     print(i.login)
            #     nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
            #     ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
              
            #     if nlk:
            #         ntlk=nlk
            #     else:
            #         ntlk=''
            #     if ncmt:
            #         ncmt=ncmt
            #     else:
            #         ncmt=''
            
            
            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''
                
            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={
                    
                    # 'ncmt':ncmt,
                    # 'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,
                    
                    'newpost':newpost,
                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    'cate':cate,
                    }
            return render(request,'createpost.html',posts)


            
        # if Interaction.objects.all():
        #     cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
        #     lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

        #     t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

        #         # tlk=Interaction.objects.values('post').order_by().annotate(Count('likes'))
        #     tlk=Interaction.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=1)[:1]
                    
        #     lks = tlk.values("post_id")
        #     tlk=Post.objects.get(id=lks)

        #     vv = t.values("post_id")
        #     trend=Post.objects.get(id=vv)

        #     posts={
        #             'tlk':tlk,
        #             'trend':trend,
        #             'lk':lk,
        #             'cmt':cmt,
        #             'posts':posts,
        #             'user':user,
        #             'cate':cate,
        #             'newpost':newpost
        #         }
        #     return render(request,'createpost.html',posts)
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

# @login_required()
def recipe(request):
    id= request.session['log_id']
    user=Login.objects.get(id=id)
    nf=''
    if Follow.objects.filter(following=user):
        nf=Follow.objects.filter(following=user).order_by("-date")[:1]
        
    else:
        nf=''
    
    if request.method=='POST' and 'search' in request.POST:
        if Post.objects.all():
            s=request.POST['search']
            posts = Post.objects.filter(name__icontains=s)
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            cate=Category.objects.all()

            if Follow.objects.filter(user=user):
                print("follow==============")
                fu=Follow.objects.filter(user=user)
                print(fu,"====-=")
                for i in fu:
                    print(i.post,"=====-p")
                    if i.post == None:
                        fnt=''
                        
                    else:
                        fnt=i
                        print(fnt,"====i")
            else:
                fnt=''
                
            if Postlike.objects.all() or Postcomment.objects.all():
            # print(posts)
            
                allposts=Post.objects.filter(login=user)
                ncmt=Postcomment.objects.none()
                ntlk=Postlike.objects.none()
                for i in allposts:
                    print(i.id)
                    print(i.login)
                    # nlk=Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                    if Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                        ntlk=ntlk|Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                        # nt=nt|ntlk
                    else:
                        ntlk=''

                    # ncmt=Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                    print(ncmt,"c======")
                        
                    if Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                        ncmt=ncmt|Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                    else:
                        ncmt='' 

                ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                print(ttlk,"ttl")
                if  ttlk:
                    lks = ttlk.values("post_id")
                    ttlk=Post.objects.get(id=lks)
                    tlk=ttlk
                    print(tlk)
                else:
                    tlk=''

                tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if  tc:
                    tr = tc.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                    if tl:
                        tr = tl.values("post_id")
                        tr=Post.objects.get(id=tr)
                        trend=tr
                    else:
                        trend=''

                posts={
                        'nf':nf,
                        'ncmt':ncmt,
                        'nlk':ntlk,
                        'tlk':tlk,
                        'trend':trend,
                        'fnt':fnt,

                        'posts':posts,
                        'cat':cate,
                        'user':user, 
                        }
                return render(request,'grid2.html',posts)

            else:
                posts={
                'nf':nf,
                'cat':cate,
                'user':user, 
                'posts':posts,
                }
                return render(request,'grid2.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Login.objects.get(id=id)
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
            user=Login.objects.get(id=id)
            cate=Category.objects.all()
            if Follow.objects.filter(user=user):
                print("follow==============")
                fu=Follow.objects.filter(user=user)
                print(fu,"====-=")
                for i in fu:
                    print(i.post,"=====-p")
                    if i.post == None:
                        fnt=''
                        
                    else:
                        fnt=i
                        print(fnt,"====i")
            else:
                fnt=''

            if Postlike.objects.all() or Postcomment.objects.all():
            # print(posts)
            
                allposts=Post.objects.filter(login=user)
                ncmt=Postcomment.objects.none()
                ntlk=Postlike.objects.none()
                for i in allposts:
                    print(i.id)
                    print(i.login)
                    # nlk=Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                    if Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                        ntlk=ntlk|Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                        # nt=nt|ntlk
                    else:
                        ntlk=''

                    # ncmt=Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                    print(ncmt,"c======")
                        
                    if Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                        ncmt=ncmt|Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                    else:
                        ncmt='' 
                    

                    

                ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                print(ttlk,"ttl")
                if  ttlk:
                    lks = ttlk.values("post_id")
                    ttlk=Post.objects.get(id=lks)
                    tlk=ttlk
                    print(tlk)
                else:
                    tlk=''

                tc=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if  tc:
                    tr = tc.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                    if tl:
                        tr = tl.values("post_id")
                        tr=Post.objects.get(id=tr)
                        trend=tr
                    else:
                        trend=''

                posts={
                        'nf':nf,
                        'ncmt':ncmt,
                        'nlk':ntlk,
                        'tlk':tlk,
                        'trend':trend,
                        'fnt':fnt,

                        'posts':posts,
                        'cat':cate,
                        'user':user, 
                        }
                return render(request,'grid2.html',posts)

            else:
                posts={
                'nf':nf,
                'cat':cate,
                'user':user, 
                'posts':posts,
                }
                return render(request,'grid2.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            posts={
                'cat':cate,
                'user':user, 
                }
            return render(request,'grid2.html',posts)


    elif Post.objects.all():
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        if Follow.objects.filter(user=user):
            print("follow==============")
            fu=Follow.objects.filter(user=user)
            print(fu,"====-=")
            for i in fu:
                print(i.post,"=====-p")
                if i.post == None:
                    fnt=''
                    
                else:
                    fnt=i
                    print(fnt,"====i")
        else:
            fnt=''

        print(fnt,"================-f")
        

        posts=Post.objects.filter(access='public').order_by("-date")
        cate=Category.objects.all() 
        ncmt=''
        ttlk=''
        ntlk=''
        nlk=''

        if Postlike.objects.all() or Postcomment.objects.all():
            # print(posts)
            uposts=Post.objects.filter(login=user).order_by("-date")[:1]
            ncmt=Postcomment.objects.none()
            ntlk=Postlike.objects.none()
            # nt=Postlike.objects.none()
            
            for i in uposts:
                print(i.id)
                print(i.login)
                # nlk=Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                if Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                    ntlk=ntlk|Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                    # nt=nt|ntlk
                else:
                    ntlk=''

                # ncmt=Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                print(ncmt,"c======")
                    
                if Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                    ncmt=ncmt|Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                else:
                    ncmt='' 
            
            print(len(ncmt),"=====len===-")
            #  print(nt,"=======n==-")

            # print("========a==")
            # a=Postlike.objects.filter().order_by('post_id')
            #.order_by(F(Count('post_id')))
            b=Postlike.objects.values('post_id').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            
            # print(b,"==========a-=-a-=-a-=a==")
            
            # for i in b:
            #     print(i)
            # print(c,"=====c=-")
            

            # ttlk=Postlike.objects.values('post').order_by().annotate(Count('post')).filter(post__count__gt=0)[:1]
            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl===========----")
           
            if  ttlk:
                # lkc = ttlk.values("post","post__count")
                lks = ttlk.values("post_id")
                print(lks,"====l----")
                ttlk=Post.objects.get(id=lks)
                print(ttlk,"====t=l--")
                tlk=ttlk 
            else:
                tlk=''

            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(tc,"==============t=c--------")
            if  tc:
                tr = tc.values("post_id")
                print(tr)
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                # tl=Postlike.objects.filter().order_by().annotate(Count('post')).filter(post__count__gt=0)[:1]
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={
                    'nf':nf,
                    'ncmt':ncmt,
                    'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,
                    'fnt':fnt,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }
            return render(request,'grid2.html',posts)

        else:
            posts={
                'nf':nf,
                'fnt':fnt,
                'posts':posts,
                'cat':cate,
                'user':user, 
                }
            
            return render(request,'grid2.html',posts)



    else:
        # cate=Category.objects.all()
        id= request.session['log_id']
        user=Signup.objects.get(id=id)
        posts={
            # 'cat':cate,
            'user':user, 
            }
        return render(request,'grid2.html',posts)
            
    # except Exception as err:
    #     print(err)

def userprofile(request):
    id= request.session['log_id']
    user=Login.objects.get(id=id)
    if request.method=='POST' and 'search' in request.POST:
        if Post.objects.all():
            s=request.POST['search']
            posts = Post.objects.filter(name__icontains=s)
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            cate=Category.objects.all()
            if Postlike.objects.all() or Postcomment.objects.all():
            # print(posts)
             
                allposts=Post.objects.all()
                for i in allposts:
                    print(i.id)
                    print(i.login)
                    nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                    ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                    # print("=------------=-=-",nlk)
                    print(nlk,"============")
                    if nlk:
                        ntlk=nlk
                        
                    else:
                        ntlk=''
                    if ncmt:
                        ncmt=ncmt
                    else:
                        ncmt=''
                

                ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                print(ttlk,"ttl")
                if  ttlk:
                    lks = ttlk.values("post_id")
                    ttlk=Post.objects.get(id=lks)
                    tlk=ttlk
                    print(tlk)
                else:
                    tlk=''

                tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if  tc:
                    tr = tc.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                    if tl:
                        tr = tl.values("post_id")
                        tr=Post.objects.get(id=tr)
                        trend=tr
                    else:
                        trend=''

                posts={
                        
                        'ncmt':ncmt,
                        'nlk':ntlk,
                        'tlk':tlk,
                        'trend':trend,

                        'posts':posts,
                        'cat':cate,
                        'user':user, 
                        }
                return render(request,'account.html',posts)

            else:
                posts={
                'cat':cate,
                'user':user, 
                'posts':posts,
                }
                return render(request,'account.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            posts={
                'cat':cate,
                'user':user, 
                }
            return render(request,'account.html',posts)


    if request.method=='POST' and 'cat' in request.POST:
        if Post.objects.all():
            cat=request.POST['cat']
            print(cat,"===============")
            posts = Post.objects.filter(login=user,category=cat)
            print(posts,"===============================post ========cat")
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            cate=Category.objects.all()
            if Postlike.objects.all() or Postcomment.objects.all():
            
             
                allposts=Post.objects.all()
                for i in allposts:
                    print(i.id)
                    print(i.login)
                    nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                    ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                    # print("=------------=-=-",nlk)
                    print(nlk,"============")
                    if nlk:
                        ntlk=nlk
                        
                    else:
                        ntlk=''
                    if ncmt:
                        ncmt=ncmt
                    else:
                        ncmt=''
                

                ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                print(ttlk,"ttl")
                if  ttlk:
                    lks = ttlk.values("post_id")
                    ttlk=Post.objects.get(id=lks)
                    tlk=ttlk
                    print(tlk)
                else:
                    tlk=''

                tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if  tc:
                    tr = tc.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                    if tl:
                        tr = tl.values("post_id")
                        tr=Post.objects.get(id=tr)
                        trend=tr
                    else:
                        trend=''

                posts={
                        
                        'ncmt':ncmt,
                        'nlk':ntlk,
                        'tlk':tlk,
                        'trend':trend,

                        'posts':posts,
                        'cat':cate,
                        'user':user, 
                        }
                return render(request,'account.html',posts)

            else:
                posts={
                'cat':cate,
                'user':user, 
                'posts':posts,
                }
                return render(request,'account.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            posts={
                'cat':cate,
                'user':user, 
                }
            return render(request,'account.html',posts)



   
    if Post.objects.all():
        id= request.session['log_id']
        user=Login.objects.get(id=id)

        posts=Post.objects.filter(login=id)
        cate=Category.objects.all()
        if Postlike.objects.all() or Postcomment.objects.all():
            allposts=Post.objects.all()
            
            for i in allposts:
                print(i.id)
                print(i.login)
                nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                # print("=------------=-=-",nlk)
                print(nlk,"============")
                if nlk:
                    ntlk=nlk
                    
                else:
                    ntlk=''
                if ncmt:
                    ncmt=ncmt
                else:
                    ncmt=''
            

            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''

            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={
                    
                    'ncmt':ncmt,
                    'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }
            return render(request,'account.html',posts) 


        # if Interaction.objects.all():
        #     cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
        #     lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

        #     t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

            
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
        #     return render(request,'account.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Signup.objects.get(id=id)
            posts=Post.objects.filter(login=id)
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
    user_id= request.session['log_id']
    user=Login.objects.get(id=user_id)
    if request.method=='POST' and 'search' in request.POST:
        s=request.POST['search']
        return redirect('/updatepost/%d'%id)
    if Post.objects.all():
        #============================
        if request.method=='POST' and 'recipe_image' in request.FILES:
            try:
                # log_id= request.session['log_id']
                ename=request.POST['recipename']
                cname=request.POST['cat']
                print(cname)
                rimg=request.FILES['recipe_image']
                print(rimg)

                dsc=request.POST['description']
                print(dsc)
                print("=-------------------p")
                

                # login=Login.objects.get(id=log_id)
                post=Post.objects.get(id=id)
                if dsc:
                    post.description=dsc
                else:
                    post.description=post.description
                if cname:
                    post.category=cname
                else:
                    post.category=post.category
                access=request.POST['access']
                if access:
                    post.access=access
                    #------------public
                else:
                    post.access=post.access


                post.name=ename
                # post.description=dsc
                post.post_image=rimg
                
                # post=Post(name=ename,description=dsc,post_image=rimg,category=cname,login=login)
                post.save()
                # return redirect('/postrecipe')
                return redirect('/updatepost/%d'%id)
            except Exception as err:
                return HttpResponse(err)

        elif request.method=='POST':
            print("=-==------------------")
            try:
                # log_id= request.session['log_id']
                ename=request.POST['recipename']
                cname=request.POST['cat']
                print(cname)
                # rimg=request.FILES['recipe_image']
                # print(rimg)

                dsc=request.POST['description']
                print("=-------------------p")
                print(dsc)
                # if dsc:
                #     pass
                # else:
                #     dsc=Post.objects.values('description',id=id)
                # print(dsc)

                # login=Login.objects.get(id=log_id)
                post=Post.objects.get(id=id)
                if dsc:
                    post.description=dsc
                else:
                    post.description=post.description
                
                # access=request.POST['access']
                # print(access,"===========")
                if 'access' in request.POST:
                    access=request.POST['access']
                    post.access=access
                    if post.access=='public':
                        fnewpost=Post.objects.get(id=id)
                        print(fnewpost)
                        fu=Follow.objects.filter(following=user)
                        print(fu,"=====f")
                        for i in fu:
                            print(i.user)
                            i.user=i.user
                            i.following=i.following
                            i.post=fnewpost
                            i.save()
                    elif post.access=='private':
                        fnewpost=Post.objects.get(id=id)
                        print(fnewpost)
                        fu=Follow.objects.filter(following=user)
                        print(fu,"=====f")
                        for i in fu:
                            # print(i.user)
                            # i.user=i.user
                            # i.following=i.following
                            i.post.delete()
                            # i.save()

                        # ===================public
                else:
                    post.access=post.access
                

                post.name=ename
                # post.description=dsc
                post.post_image=post.post_image
                post.category=cname
                post.save()
                
                return redirect('/updatepost/%d'%id)
            except Exception as err:
                return HttpResponse(err)


        user_id= request.session['log_id']
        user=Login.objects.get(id=user_id)

        posts=Post.objects.get(id=id)
        print(posts.post_image)

        cate=Category.objects.all()
        
        if Postlike.objects.all() or Postcomment.objects.all():
            allposts=Post.objects.all()
            for i in allposts:
                print(i.id)
                print(i.login)
                nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                if nlk:
                    ntlk=nlk
                    
                else:
                    ntlk=''
                if ncmt:
                    ncmt=ncmt
                else:
                    ncmt=''
            

            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''

            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={
                    
                    'ncmt':ncmt,
                    'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,

                    'posts':posts,
                    'cate':cate,
                    'user':user, 
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
    if request.method=='POST' and 'search' in request.POST:
        s=request.POST['search']
        return redirect('/updateprofile')
    if request.method=='POST' and 'user_image' in request.FILES:
        try:
            log_id= request.session['log_id']

            unm=request.POST['username']
            email=request.POST['email']
            u_img=request.FILES['user_image']

            
            log_user=Signup.objects.get(id=log_id)
            log_user.username=unm
            log_user.user_image=u_img
            log_user.save()

            user=Login.objects.get(id=log_id)
            user.username=unm
            user.email=email
            user.user_image=u_img
            user.save()
                
            return redirect('/updateprofile')
            # posts={
            #     'seml':log_user,
            #     'user':user, 
            #     }
            # return render(request,'updateprofile.html',posts) 
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

            log_user=Login.objects.get(id=log_id)
            log_user.username=unm
            log_user.save()
            return redirect('/updateprofile')
            # posts={
            #     'seml':log_user,
            #     'user':user, 
            #     }
            # return render(request,'updateprofile.html',posts) 
                
        except Exception as err:
            return HttpResponse(err)
    
    elif Post.objects.all():
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        seml=Signup.objects.get(id=id)
        posts=Post.objects.all()
        if Postlike.objects.all() or Postcomment.objects.all():
            allposts=Post.objects.all()
            
            for i in allposts:
                print(i.id)
                print(i.login)
                nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                # print("=------------=-=-",nlk)
                print(nlk,"============")
                if nlk:
                    ntlk=nlk
                    
                else:
                    ntlk=''
                if ncmt:
                    ncmt=ncmt
                else:
                    ncmt=''
            

            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''

            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={
                    
                    'ncmt':ncmt,
                    'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,
                    'seml':seml,
                    'posts':posts,
                    # 'cat':cate,
                    'user':user, 
                    }       
            return render(request,'updateprofile.html',posts)
        else:
            user=Login.objects.get(id=id)
            log_user=Signup.objects.get(login=user)
            posts={
                    'posts':posts,
                    'seml':log_user,
                    'user':user, 
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



def interactions(request,id):
    user_id= request.session['log_id']
    posts=Post.objects.get(id=id)
    user=Login.objects.get(id=user_id)
    if request.method=='POST' and 'comment' in request.POST:
        comment=request.POST['comment']
        user_id= request.session['log_id']
        post_id=Post.objects.get(id=id)
        cu=Login.objects.get(id=user_id)
        comment=Postcomment(comment=comment,user=cu,post=post_id)
        comment.save()
        return redirect('/interactions/%d'%id)

    elif request.method=='POST' and 'like' in request.POST:
        likes=request.POST['like']
        user_id= request.session['log_id']
        posts=Post.objects.get(id=id)
        user=Login.objects.get(id=user_id)
        if Postlike.objects.filter(post=posts,user=user):
            return redirect('/interactions/%d'%id)
        else:
            likes=Postlike(likes=likes,user=user,post=posts)
            likes.save()
            return redirect('/interactions/%d'%id)

    elif Postcomment.objects.all() or Postlike.objects.all():
        ntlk='',
        tlk='',
        trend='',
        nlk=''
        uposts=Post.objects.filter(login=user)
        ncmt=Postcomment.objects.none()
        ntl=Postlike.objects.none()
        print(type(ntl),"===nnn")
        for i in uposts:
            print(i.id)
            print(i.login)
            # nlk=Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                   
            if Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                print(type(ntlk),"=============n==")
                ntlk=Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                # ntlk=ntlk | ntl
            else:
                ntlk=Postlike.objects.none()

            # ncmt=Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
            print(ncmt,"c======")
                    
            if Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                ncmt=ncmt|Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
            else:
                ncmt=Postcomment.objects.none()

        ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
        print(ttlk,"ttl===========----")
        if  ttlk:
            lks = ttlk.values("post_id")
            ttlk=Post.objects.get(id=lks)
            tlk=ttlk
            print(tlk)
        else:
            tlk=''




        # cusr=Postcomment.objects.get(user=)
        # print("or =================")
        cmtp=Postcomment.objects.filter(post=id)
        # print(cmtp)
        lkp=Postlike.objects.filter(post=id)
        # print(lkp)



        


        if cmtp:
            cmtp=Postcomment.objects.filter(post=id).order_by('-date')
            print(cmtp)
        else:
            cmtp=''
        if lkp:
            count_lk=Postlike.objects.filter(post=posts).count()
            if count_lk:
                nlk=count_lk
                print(nlk)
            else:
                nlk=''


        # noti_lk=Postlike.objects.filter(~Q(user=posts.login),~Q(user=user)).order_by('-date')[:3]
        # if noti_lk:
        #     ntlk=noti_lk
        # else:
        #     ntlk=''



        # ttlk=Postlike.objects.filter().order_by().annotate(Count('likes')).filter(likes__count__gt=0)[:1]
        # print(ttlk,"ttl")
        # if  ttlk:
        #     lks = ttlk.values("post_id")
        #     ttlk=Post.objects.get(id=lks)
        #     tlk=ttlk
        #     print(tlk)
        # else:
        #     tlk=''

        tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
        print("=========",tc)
        if  tc:
            tr = tc.values("post_id")
            tr=Post.objects.get(id=tr)
            trend=tr
            print(trend,"===================================---")
        else:
            tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if tl:
                tr = tl.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                trend=''
            # trend=''
        
        posts={
                'lk':nlk,
                'nlk':ntlk,
                'tlk':tlk,
                'trend':trend,

                'cmt':cmtp,
                'posts':posts,
                'user':user,
                # 'cat':cate,
            }

        return render(request,'interactions.html',posts)

    else:
        print("else =======================")
        user_id= request.session['log_id']
        user=Login.objects.get(id=user_id)
        posts=Post.objects.get(id=id)
        posts={
            'user':user,
            'posts':posts,
        }
        return render(request,'interactions.html',posts)

def notification(request):
    if Post.objects.all():
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        if Follow.objects.filter(following=user):
            nf=Follow.objects.filter(following=user).order_by("-date")[:1]
        else:
            nf=''
        
        fnt=Follow.objects.none()
        if Follow.objects.filter(user=user):
            
            # print("follow==============")
            fu=Follow.objects.filter(user=user)
            # print(fu,"====-=")
            fnt=Follow.objects.none()
            for i in fu:
                print(i,"====i-----------------")
                print(i.post,"=====-p")
                if i.post == None:
                    fnt=fnt|fnt
                    
                    
                else:
                    print(i.id,"------i")
                    # print(type(i),"=====================i")
                    # print(type(fnt),"=====================f")
                    fnt=fnt|Follow.objects.filter(user=i.user)
                    print(fnt,"====i-----------------")
        else:
            fnt=''

        print(fnt,"================-f")
        


        posts=Post.objects.all()
        cate=Category.objects.all()
        ncmt=''
        ttlk=''
        tlk=''
        ntlk=''

        if Postlike.objects.all() or Postcomment.objects.all():
            if request.method=='POST' and 'search' in request.POST:
                s=request.POST['search']
                uposts = Post.objects.filter(login=user,name__contains=s)
            else:
                uposts=Post.objects.filter(login=user)
            # print("posts========",posts)
            
            ncmt=Postcomment.objects.none()
            ntlk=Postlike.objects.none()
            for i in uposts:
                print(i.id)
                print(i.login)
                # nlk=Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                if Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                    ntlk=ntlk|Postlike.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                    # print(ntlk,"===============-=-=-n l")
                    # nt=nt|ntlk
                else:
                    ntlk=ntlk|ntlk

                # ncmt=Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')[:3]
                # print(ncmt,"c======")
                    
                if Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date'):
                    ncmt=ncmt|Postcomment.objects.filter(~Q(user=user),post=i.id).order_by('-date')
                else:
                    ncmt=ncmt|ncmt

            # print(ncmt,"================n==c")
            # print(ntlk,"================n==l")

            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''
            # t=Postlike.objects.values('post').order_by().annotate(Count('likes')).filter(likes__count__gt=0)[:1]
            # if  t:
            #     tr = t.values("post_id")
            #     tr=Post.objects.get(id=tr)
            #     trend=tr
            #     print(trend)
            # else:
            #     trend=''
            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''
                
                
            print(ntlk,"============no=t=")
            posts={ 'nf':nf,
                    'fnt':fnt,
                    'ncmt':ncmt,
                    'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }
            return render(request,'notification.html',posts)
        else:
            posts={
                'nf':nf,
                'fnt':fnt,
                'user':user,
                'posts':posts,
            }
            return render(request,'notification.html',posts)
    else:
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        posts={
            'user':user
        }
        return render(request,'notification.html',posts)

def topten(request):
    # if request.method=='POST' and 'search' in request.POST:
    #     if Post.objects.all():
    #         s=request.POST['search']
    #         posts = Post.objects.filter(name__icontains=s)
    #         id= request.session['log_id']
    #         user=Login.objects.get(id=id)
    #         cate=Category.objects.all()
    #         if Postlike.objects.all() or Postcomment.objects.all():
    #         # print(posts)
             
    #             allposts=Post.objects.all()
    #             for i in allposts:
    #                 print(i.id)
    #                 print(i.login)
    #                 nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
    #                 ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
    #                 # print("=------------=-=-",nlk)
    #                 print(nlk,"============")
    #                 if nlk:
    #                     ntlk=nlk
                        
    #                 else:
    #                     ntlk=''
    #                 if ncmt:
    #                     ncmt=ncmt
    #                 else:
    #                     ncmt=''
                

    #             ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
    #             print(ttlk,"ttl")
    #             if  ttlk:
    #                 lks = ttlk.values("post_id")
    #                 ttlk=Post.objects.get(id=lks)
    #                 tlk=ttlk
    #                 print(tlk)
    #             else:
    #                 tlk=''

    #             tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
    #             if  tc:
    #                 tr = tc.values("post_id")
    #                 tr=Post.objects.get(id=tr)
    #                 trend=tr
    #             else:
    #                 tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
    #                 if tl:
    #                     tr = tl.values("post_id")
    #                     tr=Post.objects.get(id=tr)
    #                     trend=tr
    #                 else:
    #                     trend=''

    #             posts={
                        
    #                     'ncmt':ncmt,
    #                     'nlk':ntlk,
    #                     'tlk':tlk,
    #                     'trend':trend,

    #                     'posts':posts,
    #                     'cat':cate,
    #                     'user':user, 
    #                     }
    #             return render(request,'topten.html',posts)

    #         else:
    #             posts={
    #             'cat':cate,
    #             'user':user, 
    #             'posts':posts,
    #             }
    #             return render(request,'topten.html',posts)
    #     else:
    #         cate=Category.objects.all()
    #         id= request.session['log_id']
    #         user=Login.objects.get(id=id)
    #         posts={
    #             'cat':cate,
    #             'user':user, 
    #             }
    #         return render(request,'topten.html',posts)


    if request.method=='POST' and 'cat' in request.POST:
        if Post.objects.all():
            cat=request.POST['cat']
            print(cat,"===============")
            posts = Post.objects.filter(category=cat)
            print(posts)
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            cate=Category.objects.all()
            if Postlike.objects.all() or Postcomment.objects.all():
            
             
                allposts=Post.objects.all()
                for i in allposts:
                    print(i.id)
                    print(i.login)
                    nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                    ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                    # print("=------------=-=-",nlk)
                    print(nlk,"============")
                    if nlk:
                        ntlk=nlk
                        
                    else:
                        ntlk=''
                    if ncmt:
                        ncmt=ncmt
                    else:
                        ncmt=''
                

                ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                print(ttlk,"ttl")
                if  ttlk:
                    lks = ttlk.values("post_id")
                    ttlk=Post.objects.get(id=lks)
                    tlk=ttlk
                    print(tlk)
                else:
                    tlk=''

                tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if  tc:
                    tr = tc.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                    if tl:
                        tr = tl.values("post_id")
                        tr=Post.objects.get(id=tr)
                        trend=tr
                    else:
                        trend=''

                posts={
                        
                        'ncmt':ncmt,
                        'nlk':ntlk,
                        'tlk':tlk,
                        'trend':trend,

                        'posts':posts,
                        'cat':cate,
                        'user':user, 
                        }
                return render(request,'account.html',posts)

            else:
                posts={
                'cat':cate,
                'user':user, 
                'posts':posts,
                }
                return render(request,'account.html',posts)
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Login.objects.get(id=id)
            posts={
                'cat':cate,
                'user':user, 
                }
            return render(request,'account.html',posts)



    id= request.session['log_id']
    user=Login.objects.get(id=id)
    if Post.objects.all():
        # posts=Postcomment.objects.filter().annotate(comments=Count('post')).order_by('comments')
        ps = Post.objects.none()
        if request.method=='POST' and 'search' in request.POST:
            s=request.POST['search']
        else:
            s=''
        
        posts=Postcomment.objects.filter().order_by('post').annotate(Count('post')).filter(post__count__gt=0)
        
        for i in posts:
            print(i.post)
            if s:
                ps =ps|Post.objects.filter(id=i.post_id,name__contains=s).distinct("id")
            else:
                ps =ps|Post.objects.filter(id=i.post_id).distinct("id")


        posts=ps
        print(posts,"pp-----------------")
    
           
        cate=Category.objects.all()
        if Postlike.objects.all() or Postcomment.objects.all():
            allposts=Post.objects.all()
            
            for i in allposts:
                print(i.id)
                print(i.login)
                nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                # print("=------------=-=-",nlk)
                print(nlk,"============")
                if nlk:
                    ntlk=nlk
                    
                else:
                    ntlk=''
                if ncmt:
                    ncmt=ncmt
                else:
                    ncmt=''
            

            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''

            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={
                    
                    'ncmt':ncmt,
                    'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }
            return render(request,'topten.html',posts) 


        # if Interaction.objects.all():
        #     cmt=Interaction.objects.filter(~Q(user=user),comment__isnull=False).order_by('-date')[:5]
        #     lk=Interaction.objects.filter(~Q(user=user),likes__isnull=False).order_by('-date')[:3]

        #     t=Interaction.objects.values('post').order_by().annotate(Count('post'))[:1]

            
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
        #     return render(request,'account.html',posts)
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


def follow(request,id):
    log_id= request.session['log_id']
    user=Login.objects.get(id=log_id)
    print("-----------------1")
    follouser=Login.objects.get(id=id)
    print("-----------------2")
    


    if request.method=="POST" and "follow" in request.POST:
        following=request.POST["follow"]
        following=Login.objects.get(id=following)
        print(following,"==========flng")
        print(user)
        fll=Follow(user=user,following=following)
        fll.save()
    else:
        pass

    if request.method=="POST" and "unfollow" in request.POST:
        following=request.POST["unfollow"]
        print(following,"============f")
        Follow.objects.get(following=following,user=user).delete()
        return redirect("/follow/%d"%id)
    else:
        pass
    
    
    if Post.objects.all():
        print("follow",id)
        posts=Post.objects.filter(login=id,access='public')
        print("follow ",posts)
        cate=Category.objects.all()

        if Follow.objects.filter(user=user):
            fll=Follow.objects.filter(user=user) 
            print(follouser.id,"====u=======rid")
            # print(fll.following.id)
            for i in fll:
                print(i.following.id,"=====f--======fid")
                if follouser.id == i.following.id:
                    uf=True 
                    break  
                else:
                    uf=False
            print(uf,"====uf")
        
        else:
            print("no foloow =============")
            uf=False
            follouser=Login.objects.get(id=id)
        
        
            
        if Postlike.objects.all() or Postcomment.objects.all():
            allposts=Post.objects.all()
            
            for i in allposts:
                print(i.id)
                print(i.login)
                nlk=Postlike.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                ncmt=Postcomment.objects.filter(~Q(user=i.login),~Q(user=user)).order_by('-date')[:3]
                # print("=------------=-=-",nlk)
                print(nlk,"============")
                if nlk:
                    ntlk=nlk
                else:
                    ntlk=''
                if ncmt:
                    ncmt=ncmt
                else:
                    ncmt=''
            

            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''

            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={
                    'uf':uf,
                    'fuser':follouser,
                    'ncmt':ncmt,
                    'nlk':ntlk,
                    'tlk':tlk,
                    'trend':trend,

                    'posts':posts,
                    'cat':cate,
                    'user':user, 
                    }
            return render(request,'follow.html',posts) 


        
        else:
            cate=Category.objects.all()
            id= request.session['log_id']
            user=Signup.objects.get(id=id)
            # posts=Post.objects.all()
            posts={
                'uf':uf,
                'fuser':follouser,
                'posts':posts,
                # 'cat':cate,
                'user':user, 
                }
            return render(request,'follow.html',posts)
    else:
        posts={
                'fuser':follouser,
                'user':user, 
               }
        return render(request,'follow.html',posts) 

def followers(request):
    id= request.session['log_id']
    user=Login.objects.get(id=id)

    if Follow.objects.filter(following=user):
        fll=Follow.objects.filter(following=user).order_by("-date")
    else:
        fll=''
    if Follow.objects.filter(user=user):
        flr=Follow.objects.filter(user=user).order_by("-date")
    else:
        flr=''
        
    print(fll,"================lng-----------")
        
        
    if Post.objects.all():
        
        if Postlike.objects.all() or Postcomment.objects.all():
        
            ttlk=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            print(ttlk,"ttl")
            if  ttlk:
                lks = ttlk.values("post_id")
                ttlk=Post.objects.get(id=lks)
                tlk=ttlk
                print(tlk)
            else:
                tlk=''
           
            tc=Postcomment.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
            if  tc:
                tr = tc.values("post_id")
                tr=Post.objects.get(id=tr)
                trend=tr
            else:
                tl=Postlike.objects.values('post').order_by('post_id').annotate(Count('post')).order_by('-post__count')[:1]
                if tl:
                    tr = tl.values("post_id")
                    tr=Post.objects.get(id=tr)
                    trend=tr
                else:
                    trend=''

            posts={    
                    'flr':flr,
                    'fll':fll,
                    'tlk':tlk,
                    'trend':trend,

                    # 'posts':posts,
                    # 'cat':cate,
                    'user':user, 
                    }
            return render(request,'list_followers.html',posts)
        else:
            posts={
                'flr':flr,
                'fll':fll,
                # 'nf':nf,
                # 'fnt':fnt,
                'user':user,
                # 'posts':posts,
            }
            return render(request,'list_followers.html',posts)
    else:
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        posts={
            'flr':flr,
            'fll':fll,
            'user':user,
        }
        return render(request,'list_followers.html',posts)
