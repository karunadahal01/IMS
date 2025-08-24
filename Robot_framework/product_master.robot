*** Settings ***
Library    SeleniumLibrary
Library    Collections
Suite Setup    Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
#${URL}           https://velvet.webredirect.himshang.com.np/#/pages/dashboard
#${BROWSER}       chrome
#${USERNAME}      gedehim917@decodewp.com
#${PASSWORD}      Tebahal1!

${URL}           https://stc21.variantqa.himshang.com.np/
${BROWSER}       chrome
${USERNAME}      Sirish
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
${BARCODE_MAP}         0900
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
    Sleep    5s

    # Fill Item Details
    Input Text    xpath://input[@placeholder='Enter Item Name']    ${PRODUCT_ITEM}
    Press Keys    xpath://input[@placeholder='Enter Item Name']    TAB
    Sleep    5s
    Press Keys    xpath://input[@placeholder='Enter HS Code']    ${HS_CODE}
    Sleep    5s
    Click Element    xpath://input[@type='checkbox']  TAB
    Sleep    5s
    Press Keys    id=unit  ${UNIT}
    Sleep    5s
    Press Keys    id=ptype  ${ITEM_TYPE}
    Sleep    5s
    Press Keys    xpath://input[@placeholder='Enter Product Description']  ${DESCRIPTION}
    Sleep    5s
    Press Keys    id=Category   ${CATEGORY}
    Sleep    5s
    Press Keys    xpath://input[@placeholder='Enter Short Name']   ${SHORT_NAME}
    Sleep    5s
    Input Text    xpath://input[@type='number' and @placeholder='Enter Purchase Price']    ${PURCHASE_PRICE}
    Sleep    5s
    Input Text    xpath://input[@type='number' and @placeholder='0']    ${SALES_PRICE}
    Sleep    5s

    # Alternate Unit
    Click Element    xpath://div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']
    Sleep    5s
    Select From List By Label    xpath://select[contains(@class, 'ng-pristine')]    ${ALT_UNIT}
    Sleep    5s
    Input Text    xpath://input[@type='number' and contains(@class, 'ng-valid')]    ${CONVERSION_FACTOR}
    Sleep    5s

    # Barcode Mapping
    Click Element    xpath://div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']
    Sleep    5s
    Input Text    xpath://input[@placeholder='Enter Bar Code']    ${BARCODE_MAP}
    Sleep    5s
    Press Keys    class=form-control ng-pristine ng-valid ng-touched  ${BARCODE_UNIT}
    Click Button    id=map
    Sleep    5s

    # Save Product
    Click Button    xpath://button[contains(text(),'SAVE')]
    Sleep    5s
    Press Keys    None    ENTER
    Sleep    5s

*** Test Cases ***
Login And Add Product
    Login
    Open Product Master
    Add Product



