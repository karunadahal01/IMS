*** Settings ***
Library    SeleniumLibrary
Library    Collections
Suite Setup    Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${URL}           https://velvet.webredirect.himshang.com.np/#/pages/dashboard
${BROWSER}       chrome
${USERNAME}      gedehim917@decodewp.com
${PASSWORD}      Tebahal1!

${PRODUCT_ITEM}        Testing5610
${HS_CODE}             123
${UNIT}                kg.
${ITEM_TYPE}           Service Item
${DESCRIPTION}         This is description
${CATEGORY}            N/A
${SHORT_NAME}          XYZ
${PURCHASE_PRICE}      120
${SALES_PRICE}         140
${ALT_UNIT}            Each
${CONVERSION_FACTOR}   1000
${BARCODE_MAP}         200
${BARCODE_UNIT}        kg.

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

Login
    Wait Until Element Is Visible    css:input[formcontrolname="username"]    10s
    Input Text    css:input[formcontrolname="username"]    ${USERNAME}
    Input Text    css:input[formcontrolname="password"]    ${PASSWORD}
    Click Button    xpath://button[contains(text(), 'Sign In')]

    # Handle Already Logged In popup if present
    Run Keyword And Ignore Error    Handle Already Logged In Popup
    Log To Console    Login successful

Handle Already Logged In Popup
     Wait Until Element Is Visible    xpath=//button[.//span[text()='Logout']]    20s
    Log To Console    ✓ Already Logged In popup detected
    Click Button    xpath=//button[.//span[text()='Logout']]
    Sleep    8s
    Wait Until Element Is Visible    xpath=//button[contains(text(), 'Sign In')]    10s
    Press Keys    xpath=//button[contains(text(), 'Sign In')]    ENTER
    Sleep    20s
    Log To Console    ✓ Clicked Sign In again after logout


Open Product Master
    Click Link    Masters
    Mouse Over    link:Inventory Info
    #Sleep    4s
    Click Element    link:Product Master
#    Wait Until Element Is Visible    link:Product Master    10s
#    Click Link    Product Master
    Sleep    10s

Add Product
    Click Button    xpath://button[contains(text(), 'Add Product')]
    Sleep    2s
    Click Element   xpath://label[contains(text(), 'Add Product')]
    Execute Javascript    document.body.style.zoom="80%"
    Sleep    2s

    # Select Item Group
    Click Element    xpath://input[@placeholder='-- Press Enter For Item Group --']
    Press Keys       xpath://input[@placeholder='-- Press Enter For Item Group --']    ENTER
    Sleep    2s
    Press Keys       xpath://ng-select//input[@type='text']    ENTER
    Press Keys       xpath://ng-select//input[@type='text']    ENTER
    Sleep   5s
    Click Button     xpath://button[.//span[normalize-space()='Ok']]

    # Fill Item Details
    Input Text    xpath://input[@placeholder='Enter Item Name']    ${PRODUCT_ITEM}
    Press Keys    xpath://input[@placeholder='Enter Item Name']    TAB
    Press Keys    None    ${HS_CODE} TAB
    Click Element    xpath://input[@type='checkbox']
    Press Keys    None    ${UNIT} TAB
    Press Keys    None    ${ITEM_TYPE} TAB
    Press Keys    None    ${DESCRIPTION} TAB
    Press Keys    None    ${CATEGORY} TAB
    Press Keys    None    ${SHORT_NAME} TAB
    Input Text    xpath://input[@type='number' and @placeholder='Enter Purchase Price']    ${PURCHASE_PRICE}
    Input Text    xpath://input[@type='number' and @placeholder='0']    ${SALES_PRICE}

    # Alternate Unit
    Click Element    xpath://div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']
    Select From List By Label    xpath://select[contains(@class, 'ng-pristine')]    ${ALT_UNIT}
    Input Text    xpath://input[@type='number' and contains(@class, 'ng-valid')]    ${CONVERSION_FACTOR}

    # Barcode Mapping
    Click Element    xpath://div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']
    Input Text    xpath://input[@placeholder='Enter Bar Code']    ${BARCODE_MAP}
    Press Keys    None    TAB
    Select From List By Label    css:div.col-2.p-0 select    ${BARCODE_UNIT}
    Click Button    id:map

    # Save Product
    Click Button    xpath://button[contains(text(),'SAVE')]
    Sleep    2s
    Press Keys    None    ENTER

*** Test Cases ***
Login And Add Product
    Login
    Open Product Master
    Add Product



