*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}        https://velvet.webredirect.himshang.com.np/#/pages/dashboard
${USER}       gedehim917@decodewp.com
${PASS}       Tebahal1!

*** Test Cases ***
ERP Login With Popup Handling
    Open Browser    ${URL}    chrome
    Maximize Browser Window

    # Step 1: Enter credentials
    Wait Until Element Is Visible    css:input[formcontrolname="username"]    10s
    Input Text    css:input[formcontrolname="username"]    ${USER}
    Input Text    css:input[formcontrolname="password"]    ${PASS}
    Click Button    xpath=//button[contains(text(), 'Sign In')]

    # Step 2: Handle "Already Logged In" popup if present
    Run Keyword And Ignore Error    Handle Already Logged In Popup

    Log To Console    \n✓ Login successfully
    Sleep    30s
    Close Browser


*** Keywords ***
Handle Already Logged In Popup
    Wait Until Element Is Visible    xpath=//button[.//span[text()='Logout']]    20s
    Log To Console    ✓ Already Logged In popup detected
    Click Button    xpath=//button[.//span[text()='Logout']]
    Sleep    8s
    Wait Until Element Is Visible    xpath=//button[contains(text(), 'Sign In')]    10s
    Press Keys    xpath=//button[contains(text(), 'Sign In')]    ENTER
    Log To Console    ✓ Clicked Sign In again after logout
