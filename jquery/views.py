from django.shortcuts import render

def board(request):
    return render(request, 'jquery/board.html')

def simple_disappear(request):
    return render(request, 'jquery/simple_disappear.html')

def chainable_effects(request):
    return render(request, 'jquery/chainable_effects.html')

def accordion1(request):
    return render(request, 'jquery/accordion1.html')

def accordion2(request):
    return render(request, 'jquery/accordion2.html')

def animated_hover(request):
    return render(request, 'jquery/animated_hover.html')

def animated_hover2(request):
    return render(request, 'jquery/animated_hover2.html')

def block_clickable(request):
    return render(request, 'jquery/block_clickable.html')

def collapsible_panels(request):
    return render(request, 'jquery/collapsible_panels.html')

def illustrations(request):
    return render(request, 'jquery/illustrations.html')

def table(request):
    return render(request, 'jquery/table.html')
