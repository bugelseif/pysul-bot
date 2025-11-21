# Import do WebBot
from botcity.web import WebBot, Browser, By

# Import da integração com Orquestrador BotCity
from botcity.maestro import *

# Flag para executar localmente sem erro de autenticação
BotMaestroSDK.RAISE_NOT_CONNECTED = False

# Import do WebDriver Manager para Firefox
from webdriver_manager.firefox import GeckoDriverManager

# Import da função para converter elemento em select
from botcity.web.util import element_as_select


def main():
    # Conecta ao Orquestrador BotCity quando executado via Runner
    maestro = BotMaestroSDK.from_sys_args()
    # Retorna informações da execução
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configura modo headless do navegador
    bot.headless = True

    # Seleciona o navegador a ser utilizado
    bot.browser = Browser.FIREFOX

    # Instala o GeckoDriver para o Firefox
    bot.driver_path = GeckoDriverManager().install()


    # Lista de informações das vagas
    dados = [
        {
            "id":1,
            "jobTitle": "Training and Development Specialist",
            "jobDescription": "The responsibility of this role is to come up with structured programmes to meet the learning needs of employees.",
            "hiringDepartment": "Human Resource",
            "educationLevel": "Diploma",
            "postingStartDate": "12/10/2021",
            "postingEndDate": "30/11/2021",
            "remote": "No",
            "jobType": "Full-time"
        },
        {
            "id":2,
            "jobTitle": "Senior Software Engineer",
            "jobDescription": "This role participates in the full software development life cycle of internal enterprise applications.",
            "hiringDepartment": "Engineering",
            "educationLevel": "Degree",
            "postingStartDate": "15/10/2021",
            "postingEndDate": "14/11/2021",
            "remote": "Yes",
            "jobType": "Full-time/Permanent"
        },
        {
            "id":3,
            "jobTitle": "Accountant",
            "jobDescription": "The responsibility of this role is to provide the full spectrum of accounting support to the Head of Finance.",
            "hiringDepartment": "Finance",
            "educationLevel": "Degree",
            "postingStartDate": "24/11/2021",
            "postingEndDate": "23/12/2021",
            "remote": "No",
            "jobType": "Part-time/Temp"
        }
    ]


    # Inicia o navegador e acessa a página de login
    bot.browse("https://rpaexercise.aisingapore.org/login")

    # Realiza o login no sistema
    element = bot.find_element(selector='outlined-search', by=By.ID)
    element.send_keys("jane007")

    element = bot.find_element(selector='password', by=By.ID)
    element.send_keys("TheBestHR123")

    element = bot.find_element(selector='login', by=By.ID)
    element.click()

    # Faz um laço de repetição para cada vaga na lista de dados
    for vaga in dados:
        # Clica no botão que abre o formulário
        element = bot.find_element(selector='newJobPosting', by=By.ID)
        element.click()

        # Preenche o formulário com as informações da vaga
        element = bot.find_element(selector='jobTitle', by=By.ID)
        element.send_keys(vaga['jobTitle'])

        element = bot.find_element(selector='jobDescription', by=By.ID)
        element.send_keys(vaga['jobDescription'])

        element = bot.find_element(selector='hiringDepartment', by=By.ID)
        select_element = element_as_select(element)
        select_element.select_by_value(value=vaga['hiringDepartment'])

        element = bot.find_element(selector='educationLevel', by=By.ID)
        select_element = element_as_select(element)
        select_element.select_by_value(value=vaga['educationLevel'])

        element = bot.find_element(selector='postingStartDate', by=By.ID)
        element.send_keys(vaga['postingStartDate'])

        element = bot.find_element(selector='postingEndDate', by=By.ID)
        element.send_keys(vaga['postingEndDate'])

        # Verifica o campo Remote e clica no radio button correspondente
        if vaga["remote"] == "No":
            element = bot.find_element(selector='//input[@name="remote" and @type="radio" and @value="No"]', by=By.XPATH)
            ## Perform a default click action on the element
            element.click()
        elif vaga["remote"] == "Yes":
            element = bot.find_element(selector='//input[@name="remote" and @type="radio" and @value="Yes"]', by=By.XPATH)
            ## Perform a default click action on the element
            element.click()

        # Verifica o tipo de trabalho e clica nos checkboxes correspondentes
        if 'Full-time' in vaga["jobType"]:
            element = bot.find_element(selector='jobTypeFullTime', by=By.ID)
            element.click()
        if 'Part-time' in vaga["jobType"]:
            element = bot.find_element(selector='jobTypePartTime', by=By.ID)
            element.click()
        if 'Temp' in vaga["jobType"]:
            element = bot.find_element(selector='jobTypeTemp', by=By.ID)
            element.click()
        if 'Permanent' in vaga["jobType"]:
            element = bot.find_element(selector='jobTypePermanent', by=By.ID)
            element.click()

        # Clica em "Submit" para salvar o formulário
        element = bot.find_element(selector='submit', by=By.ID)
        element.click()

    # Aguarda 3 segundos antes de fechar o navegador
    bot.wait(3000)

    # Finaliza e encerra o navegador
    bot.stop_browser()

    # Método de finalização da tarefa no Orquestrador BotCity
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="FINALIZADO COM SUCESSO",
        total_items=3,
        processed_items=3,
        failed_items=0
    )


if __name__ == '__main__':
    main()