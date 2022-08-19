

def clicknumber(request):

    url="my-url"
    count=0
    
    if request.METHOD=='POST':
        get_link=request.POST['get_link']
        count=+1

