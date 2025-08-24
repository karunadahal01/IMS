*** Settings ***
Library           SeleniumLibrary    timeout=10
Library           String
Library           Collections
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${URL}            https://velvet.webredirect.himshang.com.np/#/pages/dashboard
${USERNAME}       gedehim917@decodewp.com
${PASSWORD}       Tebahal1!
${BROWSER}        Chrome
${WAIT_TIME}

*** Test Cases ***
Login And Create Sales Tax Invoice
    Login    ${USERNAME}    ${PASSWORD}    ${URL}
    Sales Tax Invoice    2020

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
    # Handle Already Logged In popup
    ${popup_present}=    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//button[.//span[text()='Logout']]    20s
    IF    ${popup_present}
        Log    ✓ Already Logged In popup detected
        ${logout_button}=    Get WebElement    xpath=//button[.//span[text()='Logout']]
        Click Element    ${logout_button}
        Sleep    8
        Wait Until Element Is Enabled    xpath=//button[contains(text(), 'Sign In')]    10s
        Press Key    xpath=//button[contains(text(), 'Sign In')]    \\13
        Log    ✓ Clicked Sign In again after logout
    ELSE
        Log    ℹ️ No 'Already Logged In' popup detected — continuing without logout
    END
    Log    Login successfully
    Sleep    10s

Sales Tax Invoice
    [Arguments]    ${barcode_sales}
    ${wait}=    Set Variable    ${WAIT_TIME}
    Click Link    Transactions
    Sleep    2s
    Mouse Over    link=Sales Transaction
    Sleep    5s
    Click Link    Sales Tax Invoice
    Sleep    5s

    ${random_refno}=    Generate Random String    8    [LETTERS][NUMBERS]
    Log    Generated Refno: ${random_refno}

    Clear Element Text    id=refnoInput
    Input Text    id=refnoInput    ${random_refno}
    Sleep    3s

    Click Element    id=customerselectid
    Press Key    id=customerselectid    \\13
    Sleep    5s

    Press Key    xpath=//body    \\13
    Sleep    10s

    Clear Element Text    id=remarksid
    Input Text    id=remarksid    This is an automated remark for STI.
    Sleep    5s
    Log    ✅ Remarks entered successfully.

    # Handle barcode and quantity
    Clear Element Text    id=barcodeField
    Input Text    id=barcodeField    ${barcode_sales}
    Press Key    id=barcodeField    \\13

    ${quantity}=    Evaluate    random.randint(10, 80)    modules=random
    Log    Generated quantity: ${quantity}

    ${xpaths}=    Create List
    ...    //table//tr//td[position()=9]//input
    ...    //input[contains(@name, 'quantity') or contains(@name, 'Quantity')]
    ...    //input[contains(@id, 'quantity') or contains(@id, 'Quantity')]
    ...    //td[contains(@class, 'quantity')]//input
    ...    //table//tbody//tr[1]//td[9]//input

    ${quantity_field}=    Run Keyword And Ignore Error    Find Quantity Field And Input Quantity    ${xpaths}    ${quantity}
    Run Keyword If    '${quantity_field}' == 'FAIL'    Log    ❌ Could not locate the quantity input field.

    # Show Details using F1
    Press Key    xpath=//body    \\xf1
    Sleep    5s

    ${flat_discount}=    Evaluate    random.randint(1, 50)    modules=random

    Log    Generated Flat Discount: ${flat_discount}%

    Clear Element Text    id=flatDis1
    Input Text    id=flatDis1    ${flat_discount}
    Press Key    id=flatDis1    \\13
    Sleep    3s

    Click Button    xpath=//button[text()='AFTER']
    Wait Until Element Is Enabled    xpath=//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]
    Sleep    5s

    Wait Until Element Is Enabled    xpath=//button[contains(text(), 'Balance Amount') and contains(@class, 'btn-info')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(), 'Balance Amount') and contains(@class, 'btn-info')]
    Sleep    5s

    Wait Until Element Is Enabled    xpath=//button[contains(text(), 'Add') and contains(@class, 'btn-info')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(), 'Add') and contains(@class, 'btn-info')]
    Sleep    5s

    Press Key    xpath=//body    \\ue00f    # Keys.END
    Sleep    10s

    Wait Until Element Is Enabled    xpath=//button[contains(text(), 'VIEW')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(), 'VIEW')]
    Sleep    2s

    Press Key    xpath=//body    \\13
    Sleep    5s

    Wait Until Element Is Enabled    xpath=//button[contains(text(), 'RESET')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(), 'RESET')]
    Sleep    5s

    ${alert_present}=    Run Keyword And Return Status    Alert Should Be Present    5s
    IF    ${alert_present}
           Handle Alert  #dismiss -  if you need to dismmis the alert

    END
    Sleep    5s

    Wait Until Element Is Enabled    xpath=//button[contains(text(), 'BACK')]    ${WAIT_TIME}
    Click Button    xpath=//button[contains(text(), 'BACK')]
    Sleep    3s

Find Quantity Field And Input Quantity
    [Arguments]    ${xpaths}    ${quantity}
    FOR    ${xpath}    IN    @{xpaths}
        ${status}=    Run Keyword And Ignore Error    Wait Until Element Is Enabled    xpath=${xpath}    5s
        IF    '${status[0]}' == 'PASS'
            Clear Element Text    xpath=${xpath}
            Input Text    xpath=${xpath}    ${quantity}
            Press Key    xpath=${xpath}    \\13
            Log    ✅ Quantity entered and Enter key pressed using xpath: ${xpath}
            RETURN    PASS
        END
    END
    RETURN    FAIL
