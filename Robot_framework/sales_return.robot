*** Settings ***
Library           SeleniumLibrary
Library           String
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
#${URL}            https://velvet.webredirect.himshang.com.np/#/pages/dashboard
#${USERNAME}       gedehim917@decodewp.com
#${PASSWORD}       Tebahal1!
#${BROWSER}        Chrome
#${WAIT_TIME}      10

${URL}            https://stc21.variantqa.himshang.com.np/#/
${USERNAME}       Sirish
${PASSWORD}       Tebahal1!
${BROWSER}        Chrome
${WAIT_TIME}      10

*** Test Cases ***
Login And Sales Return Full Flow
    Login    ${USERNAME}    ${PASSWORD}    ${URL}
    Sales Return Full

*** Keywords ***
Open Browser To Login Page
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window

Login
    [Arguments]    ${username}    ${password}    ${url}
    Go To    ${url}
    Wait Until Element Is Visible    css=input[formcontrolname="username"]    ${WAIT_TIME}
    Input Text    css=input[formcontrolname="username"]    ${username}
    Input Text    css=input[formcontrolname="password"]    ${password}
    Click Button    xpath=//button[contains(text(), 'Sign In')]

    ${popup_present}=    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//button[.//span[text()='Logout']]    20s
    IF    ${popup_present}
        Log    ✓ Already Logged In popup detected
        Click Button    xpath=//button[.//span[text()='Logout']]
        Sleep    8s
        Wait Until Element Is Enabled    xpath=//button[contains(text(), 'Sign In')]    10s
        Press Key    xpath=//button[contains(text(), 'Sign In')]    \\13
        Log    ✓ Clicked Sign In again after logout
        Sleep    10s
    ELSE
        Log    ℹ️ No 'Already Logged In' popup detected — continuing without logout
    END
    Log    Login successfully

Sales Return Full
    Wait Until Element Is Visible    link=Transactions    ${WAIT_TIME}
    Click Link    Transactions
    Log    Clicked on 'Transactions'
    Sleep    1s

    Mouse Over    link=Sales Transaction
    Sleep    5s

    Wait Until Element Is Visible    link=Credit Note (Sales Return)    ${WAIT_TIME}
    Click Link    link=Credit Note (Sales Return)
    Log    Clicked 'Credit Note (Sales Return)'
    Sleep    8s

    Wait Until Element Is Visible    id=refbill    ${WAIT_TIME}
    ${refbill_input}=    Get WebElement    id=refbill
    Execute Javascript    arguments[0].removeAttribute('readonly');    ${refbill_input}
    Click Element    ${refbill_input}
    Press Key    ${refbill_input}    \\13
    Sleep    2s

    Press Key    xpath=//body    \\13
    Wait Until Element Is Enabled    id=remarksid    ${WAIT_TIME}
    Clear Element Text    id=remarksid
    Input Text    id=remarksid    sales Return by automation.
    Sleep    5s
    Log    ✅ Remarks entered successfully.

    Wait Until Element Is Enabled    xpath=//button[contains(text(),'SAVE')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(),'SAVE')]
    Sleep    10s

    Wait Until Element Is Enabled    xpath=//button[contains(text(), 'BACK')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(), 'BACK')]
    Log    Keeping browser open for 15 seconds for observation...
    Sleep    15
