import requests


class DataTest:

    def __init__(self, host_api='http://testdata.qa-auto.vimpelcom.ru', api='/api', projects="/project", data="/data",
                 modules='/module'):
        self.host = host_api
        self.api = api
        self.projects = projects
        self.data = data
        self.modules = modules
        self.host_project = f'{self.host}{self.api}{self.projects}'
        self.host_module = f'{self.host}{self.api}{self.modules}'
        self.host_data = f'{self.host}{self.api}{self.data}'

    """ Методы для projects """
    # Паолучить данные используя имя проекта
    # /api/projects/filter/{name}
    def get_all_projects_filter_by_name(self, project_name=None):
        endpoint = '/filter/'
        if project_name:
            return requests.get(f"{self.host_project}s{endpoint}{project_name}")
        else:
            return "Передей project_name"

    # Получить данные по всем проектам
    # /api/projects
    def get_all_projects(self):
        return requests.get(f'{self.host_project}s')

    # Получить модули проекта по ID
    # /api/project/{projectId}
    def get_project(self, project_id=None):
        if project_id:
            return requests.get(f"{self.host_project}/{project_id}")
        else:
            return "Передей projectId"

    # Удалить данные проекта по ID
    # DELETE /api/project/{projectId}
    def delete_project(self, project_id=None):
        if project_id:
            return requests.delete(f"{self.host_project}/{project_id}")
        else:
            return "Передей projectId"

    # PUT Изменить данные проекта
    # /api/project/{projectId}
    def update_project(self, project_id=None, project_name=None, description=None):
        json_data = {"projectName": f"{str(project_name)}",
                     "description": f"{str(description)}"}
        if project_id:
            if project_name and description:
                return requests.put(f"{self.host_project}/{project_id}", json=json_data)
            elif project_name:
                return "Передай description"
            elif description:
                return "Передай project_name"
            else:
                return "Передей project_name и description"
        else:
            return "Передей projectId"

    # POST Создать новый проект
    # /api/project
    def add_project(self, project_name=None, description=None):
        json_data = {"projectName": f"{str(project_name)}",
                     "description": f"{str(description)}"}
        if project_name and description:
            return requests.post(f"{self.host_project}", json=json_data)
        elif project_name:
            return "Передай description"
        elif description:
            return "Передай project_name"

    """ Методы для module"""
    # Получить данные модуля по module_id
    # /api/module/{moduleId}
    def get_module(self, module_id=None):
        if module_id:
            return requests.get(f"{self.host_module}/{module_id}")
        else:
            return "Передай module_id"

    # Изменить данные модуля по его moduleId
    # PUT /api/module/{moduleId}
    def update_module(self, module_id=None, module_name=None, description=None):
        json_data = {
            "name": f"{str(module_name)}",
            "description": f"{str(description)}"
        }
        if module_id:
            if module_name and description:
                return requests.put(f"{self.host_module}/{module_id}", json=json_data)
            elif module_name:
                return "Передай description"
            elif description:
                return "Передай module_name"
            else:
                return "Передей module_name и description"
        else:
            return "Передей module_id"

    # Удалить модуль по его moduleId
    # DELETE /api/module/{moduleId}
    def delete_module(self, module_id=None):
        if module_id:
            return requests.delete(f"{self.host_module}/{module_id}")
        else:
            return "Передай module_id"

    # Получить информацию по всем модулям
    # /api/modules
    def get_modules(self):
        return requests.get(f"{self.host_module}s")

    # Получить информацию о модуле в проекте
    # /api/modules/{projectId}/filter/{name}
    def get_modules_filter_by_name_in_project(self, project_id=None, name=None):
        if project_id and name:
            return requests.get(f"{self.host_module}s/{project_id}/filter/{name}")
        elif project_id:
            return "Передай name"
        elif name:
            return "Передай project_id"

    # Получить все модули проекта
    # /api/modules/{projectId}
    def get_modules_in_project(self, project_id=None):
        if project_id:
            return requests.get(f"{self.host_module}s/{project_id}")
        else:
            return "Передай project_id"

    # POST Создать новый модуль в проекте
    # /api/module
    def create_module_in_project(self, project_id=None, module_name=None, description=None):
        json_data = {"name": f"{module_name}",
                     "description": f"{description}",
                     "projectId": f"{project_id}"
                     }
        if project_id:
            if module_name and description:
                return requests.post(f"{self.host_module}", json=json_data)
            elif module_name:
                return requests.post(f"{self.host_module}", json=json_data)
            elif description:
                return "Передай module_name"
        else:
            return "Передей project_id"

    """ Методы для data"""
    # Получение информации по id
    # /api/data/{dataId}
    def get_data(self, data_id=None):
        if data_id:
            return requests.get(f"{self.host_data}/{data_id}")
        else:
            return "Передай data_id"

    # Обновить данные
    # /api/data/{dataId}
    def update_data_in_project_or_module(self, data_id=None, name=None, description=None, project_id=None,
                                         module_id=None, data_json=None):
        json_data = {"name": f"{str(name)}",
                     "description": f"{str(description)}",
                     "projectId": f"{int(project_id)}",
                     "moduleId": f"{int(module_id)}",
                     "dataJson": f"{str(data_json)}"}
        if data_id:
            if project_id and module_id:
                if name and description and data_json:
                    return requests.put(f"{self.host_data}/{int(data_id)}", json=json_data)
                elif name and data_json:
                    return requests.put(f"{self.host_data}/{data_id}", json=json_data)
                else:
                    return "Передай name, description(options),data_json"
            if project_id:
                if name and description and data_json:
                    return requests.post(f"{self.host_data}", json=json_data)
                elif name and data_json:
                    return requests.post(f"{self.host_data}", json=json_data)
                else:
                    return "Передай name, description(options),data_json"
            else:
                return "Передай project_id"
        else:
            return "Передай data_id"

    # POST создание данные в модуле или проекте
    # /api/data
    def create_data_in_project_or_module(self, name=None, description=None, project_id=None, module_id=None,
                                         data_json=None):
        json_data = {"name": f"{str(name)}",
                     "description": f"{str(description)}",
                     "projectId": f"{int(project_id)}",
                     "moduleId": f"{str(module_id)}",
                     "dataJson": f"{str(data_json)}"}
        if project_id and module_id:
            if name and description and data_json:
                return requests.post(f"{self.host_data}", json=json_data)
            elif name and data_json:
                return requests.post(f"{self.host_data}", json=json_data)
            else:
                return "Передай name, description(options),data_json"
        if project_id:
            if name and description and data_json:
                return requests.post(f"{self.host_data}", json=json_data)
            elif name and data_json:
                return requests.post(f"{self.host_module}", json=json_data)
            else:
                return "Передай name, description(options),data_json"

    # Удалить data по id
    # /api/data/ {dataId}
    def delete_data(self, data_id=None):
        if data_id:
            return requests.delete(f"{self.host_data}/{data_id}")
        else:
            return "Передай data_id"

    # Показать все data
    # /api/data
    def get_all_data_in_all_projects(self):
        return requests.get(f"{self.host_data}")

    # /api/data/lock/{dataId}
    # Заброкировать data по id
    def lock_data(self, data_id=None):
        if data_id:
            return requests.put(f"{self.host_data}/lock/{data_id}")
        else:
            return "Передай data_id"

    # /api/data/unlock/{dataId}
    # Разблокировать data по id
    def unlock_data(self, data_id=None):
        if data_id:
            return requests.put(f"{self.host_data}/unlock/{data_id}")
        else:
            return "Передай data_id"

    # /api/data/random/{projectId}
    # Рандомный data из проекта (после использование его блокирует, надо юзать api_unlock_data)
    def get_random_data_in_project(self, project_id=None):
        if project_id:
            return requests.get(f"{self.host_data}/random/{project_id}")
        else:
            return "Передай project_id"

    # /api/data/randomByModule/{moduleId}
    # Рандомный data из модуля (после использование его блокирует, надо юзать api_unlock_data)
    def get_random_data_in_module(self, module_id=None):
        if module_id:
            return requests.get(f"{self.host_data}/randomByModule/{module_id}")
        else:
            return "Передай api_get_random_data_in_module"

    # Получить скрытые данные в проекте
    # /api/data/hidden/{projectId}
    def get_hidden_data_in_project(self, project_id=None):
        if project_id:
            return requests.get(f"{self.host_data}/hidden/{project_id}")
        else:
            return "Передай project_id"

    # Получить скрытые данные в модуле
    # /api/data/hiddenByModule/{moduleId}
    def get_hidden_data_in_module(self, module_id=None):
        if module_id:
            return requests.get(f"{self.host_data}/hiddenByModule/{module_id}")
        else:
            return "Передай module_id"

    # Скрыть или удалить
    # /api/data/hidden/{dataId}
    def hidden_data(self, data_id=None):
        if data_id:
            return requests.delete(f"{self.host_data}/hidden/{data_id}")
        else:
            return "Передай data_id"

    # Получить данные из проекта по названию
    # /api/data/all/{projectId}/filter/{name}
    def get_data_filter_by_name_in_project(self, project_id=None, name=None):
        if project_id and name:
            return requests.get(f"{self.host_data}/all/{project_id}/filter/{name}")
        elif project_id:
            return "Передай project_id"
        elif name:
            return "Передай name"

    # Получить все данные из проекта
    # /api/data/all/{projectId}
    def get_data_in_project(self, project_id=None):
        if project_id:
            return requests.get(f"{self.host_data}/all/{project_id}")
        else:
            return "Передай project_id"

    # Получить фильтр данных по имени в модуле
    # /api/data/allByModule/{moduleId}/filter/{name}
    def get_data_filter_by_name_in_module(self, module_id=None, name=None):
        if module_id and name:
            return requests.get(f"{self.host_data}/allByModule/{module_id}/filter/{name}")
        elif module_id:
            return "Передай module_id"
        elif name:
            return "Передай name"

    # Получить все данные по модулю
    # /api/data/allByModule/{moduleId}
    def get_all_data_in_module(self, module_id=None):
        if module_id:
            return requests.get(f"{self.host_data}/allByModule/{module_id}")
        else:
            return "Передай module_id"

    # Получить свободные данные проекта
    # /api/data/free/{projectId}
    def get_free_data_in_project(self, project_id=None):
        if project_id:
            return requests.get(f"{self.host_data}/free/{project_id}")
        else:
            return "Передай project_id"

    # Получить свободные данные из проекта по имени
    # /api/data/free/{projectId}/filter/{name}
    def get_free_data_from_the_project_by_name(self, project_id=None, name=None):
        if project_id and name:
            return requests.get(f"{self.host_data}/free/{project_id}/filter/{name}")
        elif project_id:
            return "Передай project_id"
        elif name:
            return "Передай name"

    # Получить свободные данные из модуля по имени
    # /api/data/freeByModule/{moduleId}/filter/{name}
    def get_free_data_from_the_module_by_name(self, module_id=None, name=None):
        if module_id and name:
            return requests.get(f"{self.host_data}/freeByModule/{module_id}/filter/{name}")
        elif module_id:
            return "Передай module_id"
        elif name:
            return "Передай name"

    # /api/data/freeByModule/{moduleId}
    def get_free_data_in_module(self, module_id=None):
        if module_id:
            return requests.get(f"{self.host_data}/freeByModule/{module_id}")
        else:
            return "Передай module_id"
