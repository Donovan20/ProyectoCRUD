function completar(pk, token,tipo){
    var url = "pk="+pk;
    var ajax = new XMLHttpRequest();
    console.log(url)
    //Con la funcion open decimos que metodo se usara, y a donde vamos a mandar los datos desde el cliente
    ajax.open("POST", "/autocompletar/"+tipo+"/", true);
    //Esta funcion es necesaria para poder hacer la comunicacion por POST
    ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    ajax.setRequestHeader("X-CSRFToken", token );
    ajax.send(url);
    //En esta linea, se hace un callback cada ves que el estado con la conexion cambie
    ajax.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            if(this.response != "no"){
                var respuesta = JSON.parse(this.response)
                if(tipo == 'Producto'){
                    document.getElementById("pk").value = pk
                    document.getElementById("productoE").value = respuesta.producto
                    document.getElementById("precioE").value = respuesta.precio
                    select1 = document.getElementById("sucursalE")
                    select2 = document.getElementById("categoriaE")
                    select3 = document.getElementById("proveedorE")
                    if (select1.length == 0){
                        
                        for(value in respuesta.sucursal){
                            var option = document.createElement("option");
                            option.text = respuesta.sucursal[value][1];
                            option.value = respuesta.sucursal[value][0];
                            select1.add(option);
                        }
                        for(value in respuesta.categoria){
                            var option = document.createElement("option");
                            option.text = respuesta.categoria[value][1];
                            option.value = respuesta.categoria[value][0];
                            select2.add(option);
                        }
                        for(value in respuesta.proveedor){
                            var option = document.createElement("option");
                            option.text = respuesta.proveedor[value][1];
                            option.value = respuesta.proveedor[value][0];
                            select3.add(option);
                        }
                    }
                }else if(tipo == 'Categoria'){
                    document.getElementById("pk").value = pk
                    document.getElementById("categoriaE").value = respuesta.categoria
                }else if(tipo == 'Sucursal'){
                    document.getElementById("pk").value = pk
                    document.getElementById("sucursalE").value = respuesta.sucursal
                    document.getElementById("direccionE").value = respuesta.direccion
                    document.getElementById("estadoE").value = respuesta.estado
                    document.getElementById("cpE").value = respuesta.cp
                }else if(tipo == 'Puesto'){
                    document.getElementById("pk").value = pk
                    document.getElementById("puestoE").value = respuesta.puesto
                }else if(tipo == 'Proveedor'){
                    document.getElementById("pk").value = pk
                    document.getElementById("proveedorE").value = respuesta.proveedor
                    document.getElementById("telefonoE").value = respuesta.telefono
                }else if(tipo == 'Departamento'){
                    document.getElementById("pk").value = pk
                    document.getElementById("departamentoE").value = respuesta.departamento
                    select1 = document.getElementById("sucursalE")
                    if (select1.length == 0){
                        for(value in respuesta.sucursal){
                            var option = document.createElement("option");
                            option.text = respuesta.sucursal[value][1];
                            option.value = respuesta.sucursal[value][0];
                            select1.add(option);
                        }
                    }
                }else if(tipo == 'Empleado'){
                    document.getElementById("pk").value = pk
                    document.getElementById("nombreE").value = respuesta.nombre
                    document.getElementById("apellidoE").value = respuesta.apellido
                    document.getElementById("correoE").value = respuesta.correo
                    select1 = document.getElementById("sucursalE")
                    select2 = document.getElementById("departamentoE")
                    select3 = document.getElementById("puestoE")
                    if (select1.length == 0){
                        
                        for(value in respuesta.sucursal){
                            var option = document.createElement("option");
                            option.text = respuesta.sucursal[value][1];
                            option.value = respuesta.sucursal[value][0];
                            select1.add(option);
                        }
                        for(value in respuesta.departamento){
                            var option = document.createElement("option");
                            option.text = respuesta.departamento[value][1];
                            option.value = respuesta.departamento[value][0];
                            select2.add(option);
                        }
                        for(value in respuesta.puesto){
                            var option = document.createElement("option");
                            option.text = respuesta.puesto[value][1];
                            option.value = respuesta.puesto[value][0];
                            select3.add(option);
                        }
                    }
                }
            }
        }
    }
}

function borrar(pk){
    document.getElementById('pkB').value = pk
}

function com(token,tipo){
    var ajax = new XMLHttpRequest();
    //Con la funcion open decimos que metodo se usara, y a donde vamos a mandar los datos desde el cliente
    ajax.open("POST", "/autocompletar/"+tipo+"/", true);
    //Esta funcion es necesaria para poder hacer la comunicacion por POST
    ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    ajax.setRequestHeader("X-CSRFToken", token );
    ajax.send();
    //En esta linea, se hace un callback cada ves que el estado con la conexion cambie
    ajax.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            if(this.response != "no"){
                var respuesta = JSON.parse(this.response)
                if(tipo == 'Producto'){
                    select1 = document.getElementById("id_sucursal")
                    select2 = document.getElementById("id_categoria")
                    select3 = document.getElementById("id_proveedor")
                    if (select1.length == 0){
                        
                        for(value in respuesta.sucursal){
                            var option = document.createElement("option");
                            option.text = respuesta.sucursal[value][1];
                            option.value = respuesta.sucursal[value][0];
                            select1.add(option);
                        }
                        for(value in respuesta.categoria){
                            var option = document.createElement("option");
                            option.text = respuesta.categoria[value][1];
                            option.value = respuesta.categoria[value][0];
                            select2.add(option);
                        }
                        for(value in respuesta.proveedor){
                            var option = document.createElement("option");
                            option.text = respuesta.proveedor[value][1];
                            option.value = respuesta.proveedor[value][0];
                            select3.add(option);
                        }
                    }
                }else if(tipo == 'Departamento'){
                    select1 = document.getElementById("id_sucursal")
                    if (select1.length == 0){
                        for(value in respuesta.sucursal){
                            var option = document.createElement("option");
                            option.text = respuesta.sucursal[value][1];
                            option.value = respuesta.sucursal[value][0];
                            select1.add(option);
                        }
                    }
                }else if(tipo == 'Empleado'){
                    select1 = document.getElementById("id_sucursal")
                    select2 = document.getElementById("id_departamento")
                    select3 = document.getElementById("id_puesto")
                    if (select1.length == 0){
                        
                        for(value in respuesta.sucursal){
                            var option = document.createElement("option");
                            option.text = respuesta.sucursal[value][1];
                            option.value = respuesta.sucursal[value][0];
                            select1.add(option);
                        }
                        for(value in respuesta.departamento){
                            var option = document.createElement("option");
                            option.text = respuesta.departamento[value][1];
                            option.value = respuesta.departamento[value][0];
                            select2.add(option);
                        }
                        for(value in respuesta.puesto){
                            var option = document.createElement("option");
                            option.text = respuesta.puesto[value][1];
                            option.value = respuesta.puesto[value][0];
                            select3.add(option);
                        }
                    }
                }
            }
        }
    }
}