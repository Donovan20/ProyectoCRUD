from django import forms

class ProductoForm(forms.Form):

    producto = forms.CharField(label = 'Producto',max_length= 50, widget=forms.TextInput(attrs={'class':'form-control'}))
    precio = forms.DecimalField(label = 'Precio',max_digits=6,decimal_places=2, widget=forms.NumberInput(attrs={'class':'form-control'}))
    sucursal = forms.ChoiceField(label = 'Sucursal', widget=forms.Select(attrs={'class':'form-control'}))
    categoria = forms.ChoiceField(label = 'Categoria', widget=forms.Select(attrs={'class':'form-control'}))
    proveedor = forms.ChoiceField(label = 'Proveedor', widget=forms.Select(attrs={'class':'form-control'}))

    
class ProductoFormE(forms.Form):
    producto = forms.CharField(label = 'Producto',max_length= 50, widget=forms.TextInput(attrs={'class':'form-control','id':'productoE'}))
    precio = forms.DecimalField(label = 'Precio',max_digits=6,decimal_places=2, widget=forms.NumberInput(attrs={'class':'form-control','id':'precioE'}))
    sucursal = forms.ChoiceField(label = 'Sucursal', widget=forms.Select(attrs={'class':'form-control','id':'sucursalE'}))
    categoria = forms.ChoiceField(label = 'Categoria', widget=forms.Select(attrs={'class':'form-control','id':'categoriaE'}))
    proveedor = forms.ChoiceField(label = 'Proveedor', widget=forms.Select(attrs={'class':'form-control','id':'proveedorE'}))

class CategoriaForm(forms.Form):
    categoria = forms.CharField(label = 'Categoria',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control'}))

class CategoriaFormE(forms.Form):
    categoria = forms.CharField(label = 'Categoria',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control','id':'categoriaE'}))

class SucursalForm(forms.Form):
    sucursal = forms.CharField(label = 'Sucursal',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control'}))
    direccion = forms.CharField(label = 'Direccion',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control'}))
    estado = forms.CharField(label = 'Estado',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control'}))
    cp = forms.CharField(label = 'Codigo Postal',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control'}))

class SucursalFormE(forms.Form):
    sucursal = forms.CharField(label = 'Sucursal',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control','id':'sucursalE'}))
    direccion = forms.CharField(label = 'Direccion',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control','id':'direccionE'}))
    estado = forms.CharField(label = 'Estado',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control','id':'estadoE'}))
    cp = forms.CharField(label = 'Codigo Postal',max_length= 20, widget=forms.TextInput(attrs={'class':'form-control','id':'cpE'}))

class DepartamentoForm(forms.Form):
    departamento = forms.CharField(label = 'Departamento',max_length= 30, widget=forms.TextInput(attrs={'class':'form-control'}))
    sucursal = forms.ChoiceField(label = 'Sucursal', widget=forms.Select(attrs={'class':'form-control'}))

class DepartamentoFormE(forms.Form):
    departamento = forms.CharField(label = 'Departamento',max_length= 30, widget=forms.TextInput(attrs={'class':'form-control','id':'departamentoE'}))
    sucursal = forms.ChoiceField(label = 'Sucursal', widget=forms.Select(attrs={'class':'form-control','id':'sucursalE'}))

class ProveedorForm(forms.Form):
    proveedor = forms.CharField(label = 'Proveedor',max_length= 30, widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = forms.CharField(label = 'Telefono',max_length= 30, widget=forms.TextInput(attrs={'class':'form-control'}))

class ProveedorFormE(forms.Form):
    proveedor = forms.CharField(label = 'Proveedor',max_length= 30, widget=forms.TextInput(attrs={'class':'form-control','id':'proveedorE'}))
    telefono = forms.CharField(label = 'Telefono',max_length= 30, widget=forms.TextInput(attrs={'class':'form-control','id':'telefonoE'}))

class PuestoForm(forms.Form):
    puesto = forms.CharField(label = 'Puesto',max_length= 35, widget=forms.TextInput(attrs={'class':'form-control'}))

class PuestoFormE(forms.Form):
    puesto = forms.CharField(label = 'Puesto',max_length= 35, widget=forms.TextInput(attrs={'class':'form-control','id':'puestoE'}))

class EmpleadoForm(forms.Form):
    nombre = forms.CharField(label = 'Nombre',max_length= 50, widget=forms.TextInput(attrs={'class':'form-control'}))
    apellido = forms.CharField(label = 'Apellido',max_length= 50, widget=forms.TextInput(attrs={'class':'form-control'}))
    correo = forms.CharField(label = 'Correo',max_length= 50, widget=forms.TextInput(attrs={'class':'form-control'}))
    sucursal = forms.ChoiceField(label = 'Sucursal', widget=forms.Select(attrs={'class':'form-control'}))
    departamento = forms.ChoiceField(label = 'Departamento', widget=forms.Select(attrs={'class':'form-control'}))
    puesto = forms.ChoiceField(label = 'Puesto', widget=forms.Select(attrs={'class':'form-control'}))

class EmpleadoFormE(forms.Form):
    nombre = forms.CharField(label = 'Nombre',max_length= 50, widget=forms.TextInput(attrs={'class':'form-control','id':'nombreE'}))
    apellido = forms.CharField(label = 'Apellido',max_length= 50, widget=forms.TextInput(attrs={'class':'form-control','id':'apellidoE'}))
    correo = forms.CharField(label = 'Correo',max_length= 150, widget=forms.TextInput(attrs={'class':'form-control','id':'correoE'}))
    sucursal = forms.ChoiceField(label = 'Sucursal', widget=forms.Select(attrs={'class':'form-control','id':'sucursalE'}))
    departamento = forms.ChoiceField(label = 'Departamento', widget=forms.Select(attrs={'class':'form-control','id':'departamentoE'}))
    puesto = forms.ChoiceField(label = 'Puesto', widget=forms.Select(attrs={'class':'form-control','id':'puestoE'}))