import celeryconfig                            
from celery import Celery                                  
app = Celery()                                          
app.config_from_object("celeryconfig")
i = app.control.inspect()
print "*********REGISTERED TASKS**********\n"
print i.registered()



 
