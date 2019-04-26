# coding:utf-8

from functools import partial
def outfunc(x, y=11):
    print(x, ':', y)

print('Metaclass start')
class DemoMetaClass(type):
    # something passed in as a Class declared
    def __new__(mcs, name,bases,attrs):
        # metaclass __new__() will create a new Class, in other words 
        # metaclass's instance is a NewClass but not a class's instance
        print(mcs.__name__, name, '__new__ by ', super().__name__, bases)
        print('\nattrs\n', attrs)
        print('mcs.__dict__:\n', mcs.__dict__)
        # Error here,setattr() just can called by instance increated by object, metaclass has no setattr()
        # setattr(mcs, something, something)

        # attrs['__qualname__'] = 'Nfoo' #this is immutable, and
        # other attrs can be mutable, including class's variables and functions.
        attrs['something'] = 'something'
        # dont care about cls or self argument, because interpreter can pass it in default
        metabarfunc = partial(outfunc, 'metabarfunc', y=444)
        attrs['metabarfunc'] = metabarfunc
        new_class = super(DemoMetaClass, mcs).__new__(mcs, name, bases, attrs)
        print('\nadd something attrs:\n', attrs)
        # do something with new_class
        # exp: new_class['classattrname']='value',
        # but attrs['attrname']=value does not works well, because new_class has been created.
        return new_class

    def __call__(cls, *args, **kwargs):
        print('Metaclass called\ncls.__dict__\n', cls.__dict__)
        print(cls.__name__,'__call__', args, kwargs)
        print('args:', args),
        print('kwargs:', kwargs)
        print('Foo add something:', cls.something)
        cls.xxxxx=888
        cls.barfunc = partial(outfunc, 'another xxxxxxxxxxxxxxxx', y=77777777777)
        print('\n cls.__dict__:\n', cls.__dict__)
        # before _instance created, cls can not call setattr() function
        print('\nmetaclass.__call__ declare _instance\n')
        # make a sense that when call the following code before return, interpreter will turn to call Foo.__new__() method firstly
        # and after Foo.__init__() method was done , then turn back here to keep going.
        _instance = super(DemoMetaClass, cls).__call__(*args, **kwargs)
        # do something with _instance
        # exp: setattr(_instance, 'instance_variable_name', value or function), or other methods
        # it will create some variables for _instance of the Class
        print('\nmetaclass.__call__ _instance created\n')
        print('\nmetaclass.call _instance.__dict__\n',_instance.__dict__)
        print('\nmetaclass.call _instance.dir\n', dir(_instance))
        infunc = partial(outfunc, 'self _instance func', y=8888)
        setattr(_instance, 'infunc', infunc)
        _instance.fooval = 'fooval'
        print('\nafter and infunc _instance.__dict__\n',_instance.__dict__)
        return _instance

print('\nClass Foo declaration start\n')
# `Foo` as str, `(object,[other parrent class,])` as a tuple will be passed to metaclass.__new__().
# their positons are the 2nd,3rd arg. 'something' as the 5th wihich can be arg or kwarg, etc
class Foo(object, metaclass = DemoMetaClass):
    # class variables will be passed to it's metaclasss.__new__(), as the 4th arg named `attrs`
    fields={'id':1, 'time':"12:00"}
    def __init__(self, name):        
        self.name = name
        print('\n Foo __init__ start\n')
        print('\n foo instance.__dict__\n', self.__dict__)
        print('\nfoo instance.dir\n', dir(self))
        # when return, then turn back to call the _instance creating code in methclass.__call__()

    def __new__(cls, *arg, **kwargs):
        print('\nFoo __new__ start')
        # handle cls variables or funcitons here
        print(arg, kwargs)
        print('\nFoo.__class__.__dict__ = its metaclass.__dict__:\n', Foo.__class__.__dict__)
        print('\nFoo.__dict__\n', cls.__dict__)
        # this return will call Foo's superclass and object to create a new instance as self, then call self.__init__()
        # cauttion: it's diffirent to metaclass.__new__() method
        return super(Foo, cls).__new__(cls)

    def foofunc(self, x, y=1):
        print(x, ':', y)
print('\nFoo.__dict__\n',Foo.__dict__)
print('\nFoo construct a instance start')
foo1 = Foo('jack')
print('\nFoo.__dict__\n',Foo.__dict__)
print('\nfoo1.__dict__\n',foo1.__dict__)
print(foo1.name)
Foo.barfunc()
foo1.infunc()

print('\nNewFoo construct a new Class start, then create a instance')
attrs = Foo.__dict__.copy()
attrs.update({'hasfield':True})
print('\nattrs:\n', attrs)
NewFoo = type(Foo)('NewFoo', (Foo,), attrs)
newfoo = NewFoo('micheal')
print('\nNewFoo.__dict__\n',NewFoo.__dict__)
print('\nnewfoo.__dict__\n',newfoo.__dict__)

