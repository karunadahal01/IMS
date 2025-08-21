*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    String
Library    BuiltIn
Library    OperatingSystem

Suite Setup     Open Browser To Login Page
Suite Teardown  Close Browser

*** Variables ***
${BROWSER}        Chrome
${URL}            https://velvet.webredirect.himshang.com.np/#/pages/dashboard
${USERNAME}       gedehim917@decodewp.com
${PASSWORD}       Tebahal1!

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

Login
    Wait Until Element Is Visible    css:input[formcontrolname="username"]    10s
    Input Text    css:input[formcontrolname="username"]    ${USERNAME}
    Input Text    css:input[formcontrolname="password"]    ${PASSWORD}
    Click Button    xpath=//button[contains(text(), 'Sign In')]

    ${status}=    Run Keyword And Ignore Error    Wait Until Element Is Visible    xpath=//button[.//span[text()='Logout']]    10s
    Run Keyword If    '${status}[0]'=='PASS'    Handle Already Logged In

    Log    ✓ Login successfully

Handle Already Logged In
     Wait Until Element Is Visible    xpath=//button[.//span[text()='Logout']]    20s
    Log To Console    ✓ Already Logged In popup detected
    Click Button    xpath=//button[.//span[text()='Logout']]
    Sleep    8s
    Wait Until Element Is Visible    xpath=//button[contains(text(), 'Sign In')]    10s
    Press Keys    xpath=//button[contains(text(), 'Sign In')]    ENTER
    Sleep    20s
    Log To Console    ✓ Clicked Sign In again after logout

Purchase Invoice
    Log    Navigating to Purchase Invoice
    Sleep    3s
    Click Element    xpath=//span[contains(text(), 'Transactions')]   # Adjust if needed
    Sleep    8s
    #Mouse Over   xpath=//span[contains(text(), 'Purchase Transaction')]
    Mouse Over    link:Purchase Transaction
    Sleep    8s
#   Click Element    xpath=//*[contains(text(), 'Purchase Invoice')]
    Click Element    link:Purchase Invoice
    Sleep    10s

    ${random_invoice}=    Evaluate    "INV-" + "".join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",6))    random
    Input Text    id=invoiceNO    ${random_invoice}
    Log    ✓ Invoice Number entered: ${random_invoice}
    Sleep    5s

    # Account dropdown
    Press Keys    xpath=//input[contains(@placeholder, 'Account')]    ENTER
    Sleep    6s
    Press Keys    xpath=//input[contains(@placeholder, 'Account')]    ENTER
    Sleep    6s

    Input Text    id=remarksid    This is an automated remark for PI.
    Sleep    6s

    # Barcode and quantity
    Input Text    id=barcodeField    2020
    Press Keys    id=barcodeField    ENTER
    ${quantity}=    Evaluate    random.randint(80,200)    random
    Input Text    xpath=//table//tr//td[position()=9]//input    ${quantity}
    Press Keys    xpath=//table//tr//td[position()=9]//input    ENTER
    Log      Quantity entered: ${quantity}

    # Discounts
    ${disc1}=    Evaluate    random.randint(1,50)    random
    Input Text    id=INDDISCOUNTRATE0    ${disc1}
    ${disc2}=    Evaluate    random.randint(1,50)    random
    Input Text    id=INDDISCOUNTRATE1    ${disc2}

    # Save
    Click Button    xpath=//button[contains(text(), 'SAVE')]
    Run Keyword And Ignore Error    Handle Alert

    Sleep    5s
    Press Keys    NONE    ESCAPE
    Sleep    5s

    Click Button    xpath=//button[contains(text(), 'VIEW')]
    Press Keys      NONE    ENTER
    Sleep    3s

    Click Button    xpath=//button[contains(text(), 'RESET')]
    Handle Alert

    Click Button    xpath=//button[contains(text(), 'BACK')]

Handle Alert
#    ${status}=    Run Keyword And Ignore Error    Alert Should Be Present
#    Run Keyword If    '${status}[0]'=='PASS'      Accept Alert
#     ${status}=    Run Keyword And Ignore Error    Alert Should Be Present
#     Run Keyword If    '${status}[0]'=='PASS'    Handle Alert    action=ACCEPT
      ${status}=    Run Keyword And Ignore Error    Alert Should Be Present
      Run Keyword If    '${status}[0]' == 'PASS'    Handle Alert



*** Test Cases ***
Test Purchase Invoice Flow
    Login
    Purchase Invoice
    Sleep    30s    # keep browser open for observation
