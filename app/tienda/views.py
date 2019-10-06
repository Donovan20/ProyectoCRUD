from django.shortcuts import render, redirect, HttpResponse
from app.tienda.conexion import Conexion
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from hashlib import md5
from abc import ABCMeta, abstractmethod
from json import dumps
from app.tienda.render import RenderPdf
from app.tienda.forms import ProductoFormE, ProductoForm
from app.tienda.forms import CategoriaForm, CategoriaFormE
from app.tienda.forms import SucursalForm, SucursalFormE
from app.tienda.forms import DepartamentoForm, DepartamentoFormE
from app.tienda.forms import ProveedorForm, ProveedorFormE
from app.tienda.forms import PuestoForm, PuestoFormE
from app.tienda.forms import EmpleadoForm, EmpleadoFormE
import pandas as pd

def nuevoAdmin(request):
    c = Conexion()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        pswd = nombre[0:3] + apellido [0:4] + correo[0:3]
        contra = md5(str.encode(pswd))
        contra =str(contra.hexdigest())
        query = "INSERT INTO empleado (nombreEmpleado, apellidoEmpleado, correo,pass) VALUES(\"" + nombre + "\" , \'" + apellido + "' ,\'" + correo + "' , \'" + contra +"')"
        if c.insert(query):
            return redirect('/')
        else:
            messages.error(request,'Hubo un problema, intentelo de nuevo')
    return render(request,'admin.html')

def login(request):
    
    try:
        request.session['usuario']
        return redirect('/menu/')
    except Exception:
        if request.method == 'POST':
            c = Conexion()
            usuario = request.POST['correo']
            contra = request.POST['password']
            contra = md5(str.encode(contra))
            contra =str(contra.hexdigest())
            query = "SELECT nombreEmpleado as Nombre, apellidoEmpleado as Apellido, idSucursal as Sucursal, idDepartamento as Departamento, job_id as Puesto, correo as Email from empleado WHERE correo = \"" + usuario + "\" AND pass = \"" + contra +"\""
            resultado = c.select(query)
            if resultado:
                request.session.modified = True
                request.session['usuario'] = resultado
                return redirect('/menu/')
            else:
                messages.error(request,'Datos incorrectos')
    return render(request,'login.html')

def menu(request):
    puesto = request.session['usuario']
    p = puesto[0][4]
    return render(request,'menu.html',{'p':p})

class Vista(metaclass = ABCMeta):
    @abstractmethod
    def renderizar(self):
        pass

    @abstractmethod
    def autocompletar(self):
        pass

    @abstractmethod
    def insertar(self):
        pass

    @abstractmethod
    def editar(self):
        pass

    @abstractmethod
    def eliminar(self):
        pass
    
    @abstractmethod
    def csv(self):
        pass

    @abstractmethod
    def pdf(self):
        pass

class Producto(Vista):
    __instance = None
    def __new__(cls):
        if Producto.__instance == None:
            Producto.__instance = super(Producto,cls).__new__(cls)
        return Producto.__instance

    def renderizar(self,request):
        c = Conexion()
        if request.session['usuario'][0][4] != 1 and request.session['usuario'][0][4] != 2 and request.session['usuario'][0][0] != 'admin':
            query = 'SELECT * FROM p_view'
            resultado = c.select(query)
            resultado2= c.select('DESC producto')
            return render(request,'menuView.html',{'datos':resultado,'esq':resultado2,'tabla':'Producto'})
        else:
            form = ProductoForm()
            form2 = ProductoFormE()
            query = 'SELECT p.idProducto as id, p.nombreProducto as Producto, p.precio as Precio, s.nombreSucursal as Sucursal, c.nombreCategoria as Categoria, pr.nombreProveedor as Proveedor FROM producto p, sucursal s, categoria c, proveedor pr WHERE p.idSucursal = s.idSucursal AND p.idCategoria = c.idCategoria AND p.idProveedor = pr.idProveedor ORDER BY p.idProducto'
            resultado = c.select(query)
            esquema = 'DESC producto'
            res = c.select(esquema)
            return render(request,'menuCrud.html',{'datos':resultado,'esq':res,'t':'p', 'tabla':'Producto','tipo':'producto','form':form,'form2':form2})

    def autocompletar(self,request):
        try:
            pk = request.POST['pk']
            c = Conexion()
            query = 'SELECT nombreProducto as producto, precio FROM producto WHERE idProducto = '+ pk
            resultado = c.select(query)
            query2 = 'SELECT * FROM categoria'
            resultado2 = c.select(query2)
            query3 = 'SELECT idSucursal as idS, nombreSucursal as sucursal FROM sucursal'
            resultado3 = c.select(query3)
            query4 = 'SELECT idProveedor as idP, nombreProveedor as proveedor FROM proveedor'
            resultado4 = c.select(query4)
            datos ={
                'producto': resultado[0][0],
                'precio': int(resultado[0][1]),
                'categoria':resultado2,
                'sucursal':resultado3,
                'proveedor':resultado4
            }
            return HttpResponse(dumps(datos))
        except Exception:
            c = Conexion()
            query2 = 'SELECT * FROM categoria'
            resultado2 = c.select(query2)
            query3 = 'SELECT idSucursal as idS, nombreSucursal as sucursal FROM sucursal'
            resultado3 = c.select(query3)
            query4 = 'SELECT idProveedor as idP, nombreProveedor as proveedor FROM proveedor'
            resultado4 = c.select(query4)
            datos ={
                'categoria':resultado2,
                'sucursal':resultado3,
                'proveedor':resultado4
            }
            return HttpResponse(dumps(datos))

    def editar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pk']
            producto = request.POST['producto']
            precio = request.POST['precio']
            sucursal = request.POST['sucursal']
            categoria = request.POST['categoria']
            proveedor = request.POST['proveedor']
            query = "UPDATE producto SET nombreProducto = \"" + producto + "\" , precio = " + precio + " , idSucursal = " + sucursal + " , idCategoria = " + categoria + " , idProveedor  = " + proveedor + " WHERE idProducto = " +pk
            if c.update(query):
                messages.success(request,'Producto editado correctamente')
                return redirect('/tabla/Producto/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Producto/')

    def insertar(self,request):
       c = Conexion()
       if request.method == 'POST':
            producto = request.POST['producto']
            precio = request.POST['precio']
            sucursal = request.POST['sucursal']
            categoria = request.POST['categoria']
            proveedor = request.POST['proveedor']
            query = "INSERT INTO producto (nombreProducto, precio, idSucursal, idCategoria, idProveedor) VALUES(\"" + producto + "\" , " + precio + " ," + sucursal + " ," + categoria + " ," + proveedor + ")"
            if c.insert(query):
                messages.success(request,'Producto agregado correctamente')
                return redirect('/tabla/Producto/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Producto/')

    def eliminar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pkb']
            query = "DELETE FROM producto WHERE idProducto = " + pk
            if c.delete(query):
                messages.success(request,'Producto eliminado correctamente')
                return redirect('/tabla/Producto/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Producto/')

    def csv(self,request):
        query = 'SELECT p.idProducto as id, p.nombreProducto as Producto, p.precio as Precio, s.nombreSucursal as Sucursal, c.nombreCategoria as Categoria, pr.nombreProveedor as Proveedor FROM producto p, sucursal s, categoria c, proveedor pr WHERE p.idSucursal = s.idSucursal AND p.idCategoria = c.idCategoria AND p.idProveedor = pr.idProveedor ORDER BY p.idProducto'
        c = Conexion()
        data = {}
        resultado = c.select(query)
        for r in resultado:
            if 'id' in data:
                data['id'].append(str(r[0]))
                data['producto'].append(r[1])
                data['precio'].append(str(r[2]))
                data['categoria'].append(r[3])
                data['sucursal'].append(r[4])
                data['proveedor'].append(r[5])
            else:
                
                data['id'] = [str(r[0])]
                data['producto'] = [r[1]]
                data['precio'] = [str(r[2])]
                data['categoria'] = [r[3]]
                data['sucursal'] = [r[4]]
                data['proveedor'] = [r[5]]
        cs = pd.DataFrame(data, columns= ['id','producto','precio','categoria','sucursal','proveedor'])
        cs.to_csv('static/csv/reporte.csv',sep=',')
        return redirect('/static/csv/reporte.csv')
    
    def pdf(self,request):
        query = 'SELECT p.idProducto as id, p.nombreProducto as Producto, p.precio as Precio, s.nombreSucursal as Sucursal, c.nombreCategoria as Categoria, pr.nombreProveedor as Proveedor FROM producto p, sucursal s, categoria c, proveedor pr WHERE p.idSucursal = s.idSucursal AND p.idCategoria = c.idCategoria AND p.idProveedor = pr.idProveedor ORDER BY p.idProducto'
        c = Conexion()
        resultado = c.select(query)
        query='DESC producto'
        resultado2 = c.select(query)
        params ={
            'datos':resultado,
            'esq':resultado2,
            't':'p',
            'tabla':'Producto'
        }
        return RenderPdf.render('pdf.html',params)

class Categoria(Vista):
    __instance = None
    def __new__(cls):
        if Categoria.__instance == None:
            Categoria.__instance = super(Categoria,cls).__new__(cls)
        return Categoria.__instance
    def renderizar(self,request):
        c = Conexion()
        if request.session['usuario'][0][4] != 1 and request.session['usuario'][0][4] != 2 and request.session['usuario'][0][0] != 'admin':
            query = 'SELECT * FROM c_view'
            resultado = c.select(query)
            resultado2= c.select('DESC categoria')
            return render(request,'menuView.html',{'datos':resultado,'esq':resultado2,'tabla':'Categoria'})
        else:  
            query = 'SELECT idCategoria as id, nombreCategoria as Categoria FROM categoria'
            esquema = 'DESC categoria'
            resultado = c.select(query)
            res = c.select(esquema)
            form = CategoriaForm()
            form2 = CategoriaFormE()
            return render(request,'menuCrud.html',{'datos':resultado,'t':'c','esq':res, 'tabla':'Categoria','tipo':'categoria','form':form,'form2':form2})

    def autocompletar(self,request):
        try:
            pk = request.POST['pk']
            c = Conexion()
            query = 'SELECT nombreCategoria as categoria FROM categoria WHERE idCategoria = '+ pk
            resultado = c.select(query)
            datos ={
                'categoria': resultado[0][0],
            }
            return HttpResponse(dumps(datos))
        except Exception:
            pass
            

    def editar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pk']
            categoria = request.POST['categoria']
            query = "UPDATE categoria SET nombreCategoria = \'" + categoria + "' WHERE idCategoria = " +pk
            if c.update(query):
                messages.success(request,'Categoria editada correctamente')
                return redirect('/tabla/Categoria/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Catgoria/')

    def insertar(self,request):
       c = Conexion()
       if request.method == 'POST':
            categoria = request.POST['categoria']
            query = "INSERT INTO categoria (nombreCategoria) VALUES(\'" + categoria + "')"
            if c.insert(query):
                messages.success(request,'Categoria agregada correctamente')
                return redirect('/tabla/Categoria/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Categoria/')

    def eliminar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pkb']
            query = "DELETE FROM categoria WHERE idCategoria = " + pk
            if c.delete(query):
                messages.success(request,'Categoria eliminada correctamente')
                return redirect('/tabla/Categoria/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Categoria/')

    def csv(self,request):
        query = 'SELECT idCategoria as id, nombreCategoria as categoria FROM categoria'
        c = Conexion()
        data = {}
        resultado = c.select(query)
        for r in resultado:
            if 'id' in data:
                data['id'].append(str(r[0]))
                data['categoria'].append(r[1])
            else:
                
                data['id'] = [str(r[0])]
                data['categoria'] = [r[1]]
        cs = pd.DataFrame(data, columns= ['id','categoria'])
        cs.to_csv('static/csv/reporte.csv',sep=',')
        return redirect('/static/csv/reporte.csv')
    
    def pdf(self,request):
        query = 'SELECT idCategoria as id, nombreCategoria as categoria FROM categoria'
        c = Conexion()
        resultado = c.select(query)
        query = 'DESC categoria'
        resultado2 = c.select(query)
        params ={
            'datos':resultado,
            'esq':resultado2,
            't':'c',
            'tabla':'Categoria'
        }
        return RenderPdf.render('pdf.html',params)
    

class Empleado(Vista):
    __instance = None
    def __new__(cls):
        if Empleado.__instance == None:
            Empleado.__instance = super(Empleado,cls).__new__(cls)
        return Empleado.__instance
    def renderizar(self,request):
        c = Conexion()
        query = 'SELECT e.idEmpleado as id, e.nombreEmpleado as nombre, e.apellidoEmpleado as apellido, s.nombreSucursal as sucursal, d.nombreDepartamento as departamento, p.puesto as puesto, e.correo FROM empleado e, sucursal s, puestos p, departamento d WHERE e.idSucursal = s.idSucursal AND e.idDepartamento = d.idDepartamento AND e.job_id = p.job_id ORDER BY idEmpleado'
        resultado = c.select(query)
        resultado2 = c.select('DESC empleado')
        form = EmpleadoForm()
        form2 = EmpleadoFormE()
        return render(request,'menuCrud.html',{'datos':resultado,'t':'e', 'tabla':'Empleado','tipo':'empleado','esq':resultado2,'form':form,'form2':form2})
        
    def autocompletar(self,request):
        try:
            pk = request.POST['pk']
            c = Conexion()
            query = 'SELECT nombreEmpleado as nombre, apellidoEmpleado as apellido, correo FROM empleado WHERE idEmpleado = '+ pk
            resultado = c.select(query)
            query2 = 'SELECT idDepartamento as idD, nombreDepartamento as departamento FROM departamento'
            resultado2 = c.select(query2)
            query3 = 'SELECT idSucursal as idS, nombreSucursal as sucursal FROM sucursal'
            resultado3 = c.select(query3)
            query4 = 'SELECT job_id as idP, puesto FROM puestos'
            resultado4 = c.select(query4)
            datos ={
                'nombre': resultado[0][0],
                'apellido': resultado[0][1],
                'correo':resultado[0][2],
                'departamento':resultado2,
                'sucursal':resultado3,
                'puesto':resultado4
            }
            return HttpResponse(dumps(datos))
        except Exception:
            c = Conexion()
            query2 = 'SELECT idDepartamento as idD, nombreDepartamento as departamento FROM departamento'
            resultado2 = c.select(query2)
            query3 = 'SELECT idSucursal as idS, nombreSucursal as sucursal FROM sucursal'
            resultado3 = c.select(query3)
            query4 = 'SELECT job_id as idP, puesto FROM puestos'
            resultado4 = c.select(query4)
            datos ={
                'departamento':resultado2,
                'sucursal':resultado3,
                'puesto':resultado4
            }
            return HttpResponse(dumps(datos))
    def editar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pk']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            correo = request.POST['correo']
            sucursal = request.POST['sucursal']
            puesto = request.POST['puesto']
            departamento = request.POST['departamento']
            pswd = nombre[0:3] + apellido [0:4] + correo[0:3]
            contra = md5(str.encode(pswd))
            contra =str(contra.hexdigest())
            query = "SELECT * FROM empleado WHERE correo = \'" + correo + "'"
            resultado = c.select(query)
            if resultado:
                messages.error(request,'El correo ingresado ya ha sido registrado, intente con otro')
            else:
                query = "UPDATE empleado SET nombreEmpleado = \'" + nombre + "', apellidoEmpleado = \'" + apellido + "' , correo = \'" + correo + "' , idSucursal = " + sucursal + ", job_id = " + puesto + ", idDepartamento = " + departamento + ", pass='" +contra+  "' WHERE idEmpleado = " + pk
                print(query)
                if c.update(query):
                    messages.success(request,'Empleado editado correctamente')
                    return redirect('/tabla/Empleado/')
                else:
                    messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Empleado/')

    def insertar(self,request):
       c = Conexion()
       if request.method == 'POST':
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            correo = request.POST['correo']
            sucursal = request.POST['sucursal']
            puesto = request.POST['puesto']
            departamento = request.POST['departamento']
            pswd = nombre[0:3] + apellido [0:4] + correo[0:3]
            contra = md5(str.encode(pswd))
            contra =str(contra.hexdigest())
            query = "SELECT * FROM empleado WHERE correo = \'" + correo + "'"
            resultado = c.select(query)
            if resultado:
                messages.error(request,'El correo ingresado ya ha sido registrado, intente con otro')
            else:   
                query = "INSERT INTO empleado (nombreEmpleado, apellidoEmpleado, correo, idSucursal,job_id, idDepartamento,pass) VALUES(\"" + nombre + "\" , \'" + apellido + "' ,\'" + correo + "' , " + sucursal + ",  " + puesto + ", "  +departamento +", '"+contra+"')"
                if c.insert(query):
                    messages.success(request,'Empleado agregado correctamente')
                    return redirect('/tabla/Empleado/')
                else:
                    messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Empleado/')

    def eliminar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pkb']
            query = "DELETE FROM empleado WHERE idEmpleado = " + pk
            if c.delete(query):
                messages.success(request,'Empleado eliminado correctamente')
                return redirect('/tabla/Empleado/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Empleado/')

    def csv(self,request):
        query = 'SELECT e.idEmpleado as id, e.nombreEmpleado as nombre, e.apellidoEmpleado as apellido, s.nombreSucursal as sucursal, d.nombreDepartamento as departamento, p.puesto as puesto, e.correo FROM empleado e, sucursal s, puestos p, departamento d WHERE e.idSucursal = s.idSucursal AND e.idDepartamento = d.idDepartamento AND e.job_id = p.job_id'
        c = Conexion()
        data = {}
        resultado = c.select(query)
        for r in resultado:
            if 'id' in data:
                data['id'].append(str(r[0]))
                data['nombre'].append(r[1])
                data['apellido'].append(r[2])
                data['correo'].append(r[6])
                data['sucursal'].append(r[3])
                data['departamento'].append(r[4])
                data['puesto'].append(r[5])
            else:
                
                data['id'] = (str(r[0]))
                data['nombre'] = (r[1])
                data['apellido'] = (r[2])
                data['correo'] = (r[6])
                data['sucursal'] = (r[3])
                data['departamento'] = (r[4])
                data['puesto'] = (r[5])
        cs = pd.DataFrame(data, columns= ['id','nombre','apellido','correo','sucursal','departamento','puesto'])
        cs.to_csv('static/csv/reporte.csv',sep=',')
        return redirect('/static/csv/reporte.csv')
    
    def pdf(self,request):
        query = 'SELECT e.idEmpleado as id, e.nombreEmpleado as nombre, e.apellidoEmpleado as apellido, s.nombreSucursal as sucursal, d.nombreDepartamento as departamento, p.puesto as puesto, e.correo FROM empleado e, sucursal s, puestos p, departamento d WHERE e.idSucursal = s.idSucursal AND e.idDepartamento = d.idDepartamento AND e.job_id = p.job_id'
        c = Conexion()
        resultado = c.select(query)
        query = 'DESC empleado'
        resultado2 = c.select(query)
        params ={
            'datos':resultado,
            'esq':resultado2,
            't':'e',
            'tabla':'Empleado'
        }
        return RenderPdf.render('pdf.html',params)

class Sucursal(Vista):
    __instance = None
    def __new__(cls):
        if Sucursal.__instance == None:
            Sucursal.__instance = super(Sucursal,cls).__new__(cls)
        return Sucursal.__instance

    def renderizar(self,request):
        c = Conexion()
        if request.session['usuario'][0][4] != 1 and request.session['usuario'][0][4] != 2 and request.session['usuario'][0][0] != 'admin':
            query = 'SELECT * FROM s_view'
            resultado = c.select(query)
            resultado2= c.select('DESC sucursal')
            return render(request,'menuView.html',{'datos':resultado,'esq':resultado2,'tabla':'Producto'})
        else:
            query = 'SELECT idSucursal as id, nombreSucursal as Sucursal, direccion, estado, codigoPostal as cp FROM sucursal'
            resultado = c.select(query)
            query = 'DESC sucursal'
            esq = c.select(query)
            form = SucursalForm
            form2 = SucursalFormE
            return render(request,'menuCrud.html',{'datos':resultado,'t':'s', 'tabla':'Sucursal','tipo':'sucursal','esq':esq,'form':form,'form2':form2})

    def autocompletar(self,request):
        try:
            pk = request.POST['pk']
            c = Conexion()
            query = 'SELECT nombreSucursal as sucursal, direccion,estado, codigoPostal as cp FROM sucursal WHERE idSucursal = '+ pk
            resultado = c.select(query)
            datos ={
                'sucursal': resultado[0][0],
                'direccion': resultado[0][1],
                'estado': resultado[0][2],
                'cp': resultado[0][3],
            }
            return HttpResponse(dumps(datos))
        except Exception:
            pass
            

    def editar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pk']
            sucursal = request.POST['sucursal']
            direccion = request.POST['direccion']
            estado = request.POST['estado']
            cp = request.POST['cp']
            query = "UPDATE sucursal SET nombreSucursal = \'" + sucursal + "', direccion = \'" + direccion + "' , estado = \'" + estado + "' ,codigoPostal = " + cp +" WHERE idSucursal = " + pk
            print(query)
            if c.update(query):
                messages.success(request,'Sucursal editada correctamente')
                return redirect('/tabla/Sucursal/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Sucursal/')

    def insertar(self,request):
       c = Conexion()
       if request.method == 'POST':
            sucursal = request.POST['sucursal']
            direccion = request.POST['direccion']
            estado = request.POST['estado']
            cp = request.POST['cp']
            query = "INSERT INTO sucursal (nombreSucursal, direccion, estado, codigoPostal) VALUES(\"" + sucursal + "\" , \'" + direccion + "' ,\'" + estado + "' , " + cp +")"
            print(query)
            if c.insert(query):
                messages.success(request,'Sucursal agregada correctamente')
                return redirect('/tabla/Sucursal/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Sucursal/')

    def eliminar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pkb']
            query = "DELETE FROM sucursal WHERE idSucursal = " + pk
            if c.delete(query):
                messages.success(request,'Sucursal eliminada correctamente')
                return redirect('/tabla/Sucursal/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Sucursal/')

    def csv(self,request):
        query = 'SELECT idSucursal as id, nombreSucursal as sucursal, direccion, estado, codigoPostal as cp FROM sucursal'
        c = Conexion()
        data = {}
        resultado = c.select(query)
        for r in resultado:
            if 'id' in data:
                data['id'].append(str(r[0]))
                data['sucursal'].append(r[1])
                data['direccion'].append(r[2])
                data['estado'].append(r[3])
                data['cp'].append(str(r[4]))
            else:
                
                data['id'] = [str(r[0])]
                data['sucursal'] = [r[1]]
                data['direccion'] = [r[2]]
                data['estado'] = [r[3]]
                data['cp'] = [str(r[4])]
        cs = pd.DataFrame(data, columns= ['id','sucursal','direccion','estado','cp'])
        cs.to_csv('static/csv/reporte.csv',sep=',')
        return redirect('/static/csv/reporte.csv')
    
    def pdf(self,request):
        query = 'SELECT idSucursal as id, nombreSucursal as Sucursal, direccion, estado, codigoPostal as cp FROM sucursal'
        c = Conexion()
        resultado = c.select(query)
        query = 'DESC sucursal'
        resultado2 = c.select(query)
        params ={
            'datos':resultado,
            'esq':resultado2,
            't':'s',
            'tabla':'Sucursal'
        }
        return RenderPdf.render('pdf.html',params)

class Departamento(Vista):
    __instance = None
    def __new__(cls):
        if Departamento.__instance == None:
            Departamento.__instance = super(Departamento,cls).__new__(cls)
        return Departamento.__instance

    def renderizar(self,request):
        c = Conexion()    
        query = 'SELECT d.idDepartamento as id, d.nombreDepartamento as departamento, s.nombreSucursal as sucursal FROM departamento d, sucursal s WHERE d.idSucursal = s.idSucursal ORDER BY d.idDepartamento'
        resultado = c.select(query)
        query = 'DESC departamento'
        resultado2 = c.select(query)
        form = DepartamentoForm()
        form2 = DepartamentoFormE()
        return render(request,'menuCrud.html',{'datos':resultado,'t':'d', 'tabla':'Departamento','tipo':'departamento','esq':resultado2, 'form':form,'form2':form2})
    
    def autocompletar(self,request):
        try:
            pk = request.POST['pk']
            c = Conexion()
            query = 'SELECT nombreDepartamento as departamento FROM departamento WHERE idDepartamento = '+ pk
            resultado = c.select(query)
            query3 = 'SELECT idSucursal as idS, nombreSucursal as sucursal FROM sucursal'
            resultado3 = c.select(query3)
            
            datos ={
                'departamento': resultado[0][0],
                'sucursal':resultado3,
            }
            return HttpResponse(dumps(datos))
        except Exception:
            c = Conexion()
            query3 = 'SELECT idSucursal as idS, nombreSucursal as sucursal FROM sucursal'
            resultado3 = c.select(query3)
            datos ={
                'sucursal':resultado3
            }
            return HttpResponse(dumps(datos))
    
    def editar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pk']
            departamento = request.POST['departamento']
            sucursal = request.POST['sucursal']
            query = "UPDATE departamento SET nombreDepartamento = \"" + departamento + "\" , idSucursal = " + sucursal + " WHERE idDepartamento = " +pk
            if c.update(query):
                messages.success(request,'Departamento editado correctamente')
                return redirect('/tabla/Departamento/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Departamento/')

    def insertar(self,request):
       c = Conexion()
       if request.method == 'POST':
            departamento = request.POST['departamento']
            sucursal = request.POST['sucursal']
            query = "INSERT INTO departamento (nombreDepartamento, idSucursal) VALUES(\"" + departamento + "\" , " + sucursal + ")"
            if c.insert(query):
                messages.success(request,'Departamento insertado correctamente')
                return redirect('/tabla/Departamento/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Departamento/')

    def eliminar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pkb']
            query = "DELETE FROM departamento WHERE idDepartamento = " + pk
            if c.delete(query):
                messages.success(request,'Departamento eliminado correctamente')
                return redirect('/tabla/Departamento/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Departamento/')

    def csv(self,request):
        query = 'SELECT d.idDepartamento as id, d.nombreDepartamento as departamento, s.nombreSucursal as sucursal FROM departamento d, sucursal s WHERE d.idSucursal = s.idSucursal ORDER BY d.idDepartamento'
        c = Conexion()
        data = {}
        print(query)
        resultado = c.select(query)
        for r in resultado:
            if 'id' in data:
                data['id'].append(str(r[0]))
                data['departamento'].append(r[1])
                data['sucursal'].append(r[2])
            else:
                
                data['id'] = [str(r[0])]
                data['departamento'] = [r[1]]
                data['sucursal'] = [r[2]]
        cs = pd.DataFrame(data, columns= ['id','departamento','sucursal'])
        cs.to_csv('static/csv/reporte.csv',sep=',')
        return redirect('/static/csv/reporte.csv')
    
    def pdf(self,request):
        query = 'SELECT d.idDepartamento as id, d.nombreDepartamento as departamento, s.nombreSucursal as sucursal FROM departamento d, sucursal s WHERE d.idSucursal = s.idSucursal ORDER BY d.idDepartamento'
        c = Conexion()
        resultado = c.select(query)
        query = 'DESC departamento'
        resultado2 = c.select(query)
        params ={
            'datos':resultado,
            'esq':resultado2,
            't':'d',
            'tabla':'Departamento'
        }
        return RenderPdf.render('pdf.html',params)

class Proveedor(Vista):

    __instance = None
    def __new__(cls):
        if Proveedor.__instance == None:
            Proveedor.__instance = super(Proveedor,cls).__new__(cls)
        return Proveedor.__instance

    def renderizar(self,request):
        c = Conexion()    
        query = 'SELECT idProveedor as id, nombreProveedor as proveedor, telefono FROM proveedor'
        resultado = c.select(query)
        query = 'DESC proveedor'
        resultado2 = c.select(query)
        form = ProveedorForm()
        form2 = ProveedorFormE()
        return render(request,'menuCrud.html',{'datos':resultado,'t':'pr', 'tabla':'Proveedor','tipo':'proveedor','esq':resultado2,'form':form,'form2':form2})

    def autocompletar(self,request):
        try:
            pk = request.POST['pk']
            c = Conexion()
            query = 'SELECT nombreProveedor as proveedor, telefono FROM proveedor WHERE idProveedor = '+ pk
            resultado = c.select(query)
            datos ={
                'proveedor': resultado[0][0],
                'telefono': resultado[0][1],
            }
            return HttpResponse(dumps(datos))
        except Exception:
            pass
            

    def editar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pk']
            proveedor = request.POST['proveedor']
            telefono = request.POST['telefono']
            query = "UPDATE proveedor SET nombreProveedor = \'" + proveedor + "', telefono = \'" + telefono + "'  WHERE idProveedor = " +pk
            print(query)
            if c.update(query):
                messages.success(request,'Proveedor editado correctamente')
                return redirect('/tabla/Proveedor/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Proveedor/')

    def insertar(self,request):
       c = Conexion()
       if request.method == 'POST':
            proveedor = request.POST['proveedor']
            telefono = request.POST['telefono']
            query = "INSERT INTO proveedor (nombreProveedor,telefono) VALUES(\'" + proveedor + "', \'"+ telefono +"')"
            if c.insert(query):
                messages.success(request,'Proveedor agregado correctamente')
                return redirect('/tabla/Proveedor/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Proveedor/')

    def eliminar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pkb']
            query = "DELETE FROM proveedor WHERE idProveedor = " + pk
            if c.delete(query):
                messages.success(request,'Proveedor eliminado correctamente')
                return redirect('/tabla/Proveedor/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Proveedor/')

    def csv(self,request):
        query = 'SELECT idProveedor as id, nombreProveedor as proveedor, telefono FROM proveedor'
        c = Conexion()
        data = {}
        resultado = c.select(query)
        for r in resultado:
            if 'id' in data:
                data['id'].append(str(r[0]))
                data['proveedor'].append(r[1])
                data['telefono'].append(r[2])
            else:
                
                data['id'] = [str(r[0])]
                data['proveedor'] = [r[1]]
                data['telefono'] = [r[2]]
        cs = pd.DataFrame(data, columns= ['id','proveedor','telefono'])
        cs.to_csv('static/csv/reporte.csv',sep=',')
        return redirect('/static/csv/reporte.csv')
    
    def pdf(self,request):
        query = 'SELECT idProveedor as id, nombreProveedor as proveedor, telefono FROM proveedor'
        c = Conexion()
        resultado = c.select(query)
        resultado2 = c.select('DESC proveedor')
        params ={
            'datos':resultado,
            'esq':resultado2,
            't':'pr',
            'tabla':'Proveedor'
        }
        return RenderPdf.render('pdf.html',params)

class Puesto(Vista):

    __instance = None
    def __new__(cls):
        if Puesto.__instance == None:
            Puesto.__instance = super(Puesto,cls).__new__(cls)
        return Puesto.__instance

    def renderizar(self,request):
        c = Conexion()    
        query = 'SELECT job_id as id, puesto FROM puestos'
        resultado = c.select(query)
        resultado2 = c.select('DESC puestos')
        form = PuestoForm()
        form2 = PuestoFormE()
        return render(request,'menuCrud.html',{'datos':resultado,'t':'pu', 'tabla':'Puesto','tipo':'puesto','esq':resultado2,'form':form,'form2':form2})

    def autocompletar(self,request):
        try:
            pk = request.POST['pk']
            c = Conexion()
            query = 'SELECT puesto FROM puestos WHERE job_id = '+ pk
            resultado = c.select(query)
            datos ={
                'puesto': resultado[0][0],
            }
            return HttpResponse(dumps(datos))
        except Exception:
            pass
            

    def editar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pk']
            puesto = request.POST['puesto']
            query = "UPDATE puestos SET puesto = \'" + puesto + "' WHERE job_id = " +pk
            if c.update(query):
                messages.success(request,'Puesto editado correctamente')
                return redirect('/tabla/Puesto/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Puesto/')

    def insertar(self,request):
       c = Conexion()
       if request.method == 'POST':
            puesto = request.POST['puesto']
            query = "INSERT INTO puestos (puesto) VALUES(\'" + puesto + "')"
            if c.insert(query):
                messages.success(request,'Puesto agregado correctamente')
                return redirect('/tabla/Puesto/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Puesto/')

    def eliminar(self,request):
        c = Conexion()
        if request.method == 'POST':
            pk = request.POST['pkb']
            query = "DELETE FROM puestos WHERE job_id = " + pk
            if c.delete(query):
                messages.success(request,'Puesto eliminado correctamente')
                return redirect('/tabla/Puesto/')
            else:
                messages.error(request,'Hubo un problema, intentelo de nuevo')
            return redirect('/tabla/Puesto/')

    def csv(self,request):
        query = 'SELECT job_id as id, puesto FROM puestos'
        c = Conexion()
        data = {}
        resultado = c.select(query)
        for r in resultado:
            if 'id' in data:
                data['id'].append(str(r[0]))
                data['puesto'].append(r[1])
            else:
                
                data['id'] = [str(r[0])]
                data['puesto'] = [r[1]]
        cs = pd.DataFrame(data, columns= ['id','puesto'])
        cs.to_csv('static/csv/reporte.csv',sep=',')
        return redirect('/static/csv/reporte.csv')
    
    def pdf(self,request):
        query = 'SELECT job_id as id, puesto FROM puestos'
        c = Conexion()
        resultado = c.select(query)
        resultado2 = c.select('DESC puestos')
        params ={
            'datos':resultado,
            'esq':resultado2,
            't':'pu',
            'tabla':'Puesto'
        }
        return RenderPdf.render('pdf.html',params)

def VistaFactory(request,tipo):
    return eval(tipo)().renderizar(request)

def CompletarFactory(request,tipo):
    return eval(tipo)().autocompletar(request)

def EditarFactory(request,tipo):
    return eval(tipo)().editar(request)

def EliminarFactory(request,tipo):
    return eval(tipo)().eliminar(request)

def AgregarFactory(request,tipo):
    return eval(tipo)().insertar(request)

def CsvFactory(request,tipo):
    return eval(tipo)().csv(request)

def PdfFactory(request,tipo):
    return eval(tipo)().pdf(request)

def deslogear(request):
    c = Conexion()
    c.desconectar()
    del request.session['usuario']
    return redirect('/')