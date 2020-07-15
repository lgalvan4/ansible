# Playbooks importables 

Estos playbooks estan diseñados para ser utilizados dentro de otros playbooks

## Como empezar

Descargue el repositorio a su equipo y genere su propio archivo .yml con lo que requiera que este haga.

Declara las variables que requerira el playbook a importar.

```
  tasks:
    - name: Test foo
      register: res
      command: "echo 'foo'"

    - set_fact: msj="{{ res }}"
```

Importa la tarea o playbook que requieras dentro de tu archivo:

```
    - import_tasks: plays/playbook.yml
```

## Documenteacion de cada playbook:

>### sendmail.yml

Este playboook te permite enviar correos desde Ansible-AWX desde la cuenta de kai@kionetworks.com sin necesidad de ingresar credenciales.

Las variables que admite son las siguientes:

- **para** - *Lista de emails a los que se les enviara el correo. (Requerido)*

- **conCopia** - *Lista de emails a los que se les enviara una copia. (Opcional)*

- **asunto** - *Asunto del correo. (Requerido)*

- **mensaje** - *Contenido del correo. (Requerido)*

- **adjuntos** - *Lista de ubicaciones (path) de los archivos a adjuntar. (Opcional)*

### Ejemplos de uso

Enviando un simple correo a foo@test.com

```
---
- name: Envia Correo
  hosts: all
  vars:
    # Variables fijas que se utilizaran en la importacion 
    para: <foo@test.com>
    asunto: Prueba
    mensaje: vacio

  gather_facts: false

  #Se envia un echo a el/los servers que se definan en la ejecucion 
  tasks:
    - name: Sending echo to servers
      #Guardando salida en res
      register: res
      command: "echo 'contenido del mail'"

    #Se establece la variable mensaje
    - set_fact: mensaje="{{ res }}"

    #Se importa y ejecuta el playbook 
    - import_tasks: plays/sendmail.yml
      vars:
        mensaje: "{{ mensaje }}"
```

## Authors

* **Erick Benitez** - *Playbooks: sendmail.yml*
