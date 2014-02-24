# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render_to_response
from createNote.models import Note
from django.db.models import Q
from django.http.response import HttpResponseRedirect, HttpResponse
from createNote.custom_validate import i_invalidFieldException, i_validateField
def v_search_home(req):
    if req.method=="POST":
        search_term=req.POST.get('search_term','')
        notes=search(search_term)
        return render_to_response('search_home.html',{'req':req,'notes':notes,'bypost':True,'search_term':search_term})
    return render_to_response('search_home.html') 


def search(search_term):
    '''
    NOTE : return all data if search_term=''(blank )
    else return filtered result
    
    first filter by whole "search_term"(can be a complete sentence) if not found then 
    filter by each word of "search_term"   
    '''
    search_term=search_term.strip()
    data=Note.objects.filter(Q(title__icontains=search_term)|Q(keywords__icontains=search_term)|Q(category__icontains=search_term))
    if data:return data.order_by('-last_edit')
    else:
        print "result :by word"
        hw=['am', 'are', 'is', 'was', 'were', 'be', 'being', 'been','have', 'has', 'had','shall', 'will','do', 'does', 'did','may', 'must', 'might','can', 'could', 'would', 'should','and']
        search_term=[w.lower() for w in search_term.split(' ') if w.lower() not in hw]
        print search_term
        for w in search_term:
            data=Note.objects.filter(
                                     Q(title__icontains=w)|
                                     Q(keywords__icontains=w)|
                                     Q(category__icontains=w)
                                     )
            if data:return data.order_by('-last_edit')
            
        
      
def v_show_content(req,note_id):
    return render_to_response('content.html',{'note':Note.objects.get(id=note_id),'req':req})
    
            
def v_edit_content(req,note_id):
    edit=True
    n=Note.objects.get(id=note_id)
    title=n.title
    category=n.category
    keywords=n.keywords
    content=n.content
    
    if req.method=="POST" and Note.objects.get(id=note_id).owner==req.user:
        errors=[]
        
        title=req.POST.get('title','')
        category=req.POST.get('category','')
        keywords=req.POST.get('keywords','')
        content=req.POST.get('content','')
        try:
            title=i_validateField(req.POST.get('title','').strip(),'s','title')
            category=i_validateField(req.POST.get('category','').strip(),'s','category')
            keywords=i_validateField(req.POST.get('keywords','').strip(),'s','keywords')
            content=i_validateField(req.POST.get('content','').strip(),'s','content')
        except i_invalidFieldException,e:
            errors.append(e.error_msg())
            return render_to_response('content_edit.html',locals())
        
        if not errors:
            n.title=title
            n.category=category
            n.keywords=keywords
            n.content=content
            n.save()
            return HttpResponseRedirect('/content/id_'+note_id)
    else:
        return render_to_response('content_edit.html',locals())
    

def v_add_content(req):
    add=True
    if req.method=="POST" and req.user.is_authenticated():
        #mark page as (add page)
        errors=[]
        
        try:
            title=i_validateField(req.POST.get('title','').strip(),'s','title')
            category=i_validateField(req.POST.get('category','').strip(),'s','category')
            keywords=i_validateField(req.POST.get('keywords','').strip(),'s','keywords')
            content=i_validateField(req.POST.get('content','').strip(),'s','content')
        except i_invalidFieldException,e:
            errors.append(e.error_msg())
            return render_to_response('add_content.html',locals())
        
        if not errors:
            n=Note(
                   title=title,
                   category=category,
                   keywords=keywords,
                   content=content,
                   owner=req.user
                   )
            n.save()
            return HttpResponseRedirect('/content/id_'+str(n.id))
    return render_to_response('add_content.html',locals())



def v_logout(req):
    logout(req)
    return HttpResponseRedirect('/')


def v_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    errors=[]    
    if request.method=="POST":
        
        
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','').strip()
        
        if not username or not password:
            errors.append('Please enter your username and password .')
            
        if not errors:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    errors.append("Your account is  temporary disabled . ")
            else:
                errors.append("Invalid username Or password . ")
            
    return render_to_response('login.html',{'errors':errors})