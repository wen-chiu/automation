*** Settings ***
Documentation     Warranty Check Test Plan on Chrome
# To-DO extend to other browser ex. IE, Safari, Firefox... in future

Library           Selenium2Library

Suite Setup    Open Browser    https://www.barco.com/en/clickshare/support/warranty-info    ${BROWSER}
Suite Teardown    Close Browser

*** Variables ***
${BROWSER}                  chrome
${CORRECT_SERIAL_NUM}       correct
${WRONG_SERIAL_NUM}         zzzzzzz
${EXPECT_OUT}               Description
${MAX_NUMBERS}              100
${LONG_SERIAL_NUM}          sdfdscsddfafekewlmkewlfmakwemfwe,f,ccmdsewjfoejifjwiorjflmkmvkadsmv.,xm,.zijoirwjfioeffdlmckdmc,vm.,mvwhgwurfkfmdklmnvnir
${CHINESE_CHAR} =	        我是序列號碼


*** Test Cases ***

Pre Block Serial Number Check
    [Template]    Expect Empty Warranty Output Template
    aabbc
    ${SPACE * 20}
    ${Empty}
    ${true}

Incorrect Serial Number Check
    [Template]    Expect No Find Warranty Output Template
    ${WRONG_SERIAL_NUM}
    ${LONG_SERIAL_NUM}
    ${CHINESE_CHAR}

Correct Serial Number Check

    Type Warranty        ${CORRECT_SERIAL_NUM}
    Wait Until Element Is Visible             xpath = //div [@class='o-media__body-wrapper']    30
    Element Should Contain         xpath = //div [@class='o-media__body-wrapper']    ${EXPECT_OUT}


*** Keywords ***

Expect No Find Warranty Output Template
    [Documentation]    Tempalte for unput incorrect serial number and expect no output from page
    [Arguments]    ${serial_num}
    Type Warranty        ${serial_num}
    Expected Error Message

Expect Empty Warranty Output Template
    [Documentation]    Tempalte for unput incorrect serial number and expect no output from page
    [Arguments]    ${serial_num}
    Type Warranty        ${serial_num}
    Expected No Message

Type Warranty
    [Arguments]        ${serial_num}
    Input Text               id=SerialNumber          ${serial_num}
    Click Element            xpath = //div [@class='form-group-compact form-group--no-lbl col-md-5']/button [@class='btn btn-primary btn-block btn--icon btn--arrow']

Expected Error Message
    Element Should Not Be Visible             xpath = //div [@class='o-media__body-wrapper']
    ${out} =  Get Text     xpath = //div [@data-bind='html: emptyResultText']   
    Wait Until Element Contains    xpath = //div [@data-bind='html: emptyResultText']     We couldn't find a product with this serial number    10
    ${out} =  Get Text     xpath = //div [@data-bind='html: emptyResultText']

Expected No Message
    Element Should Not Be Visible             xpath = //div [@class='o-media__body-wrapper']
    Wait Until Element Is Not Visible         xpath = //div [@data-bind='html: emptyResultText']     10
