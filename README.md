# ZOYI_backend
Channel.io Backend task

- Language : PYTHON ( Django )
- API : detectlanguage
- DB : SQLite

- Assumed thing
  - Characters such as tab and \n are not included in the input.
  - Translation POST for particular keyId is performed only once per locale.

----------------------------------------------------------------------------------------------------------------

- Excute method
  - Create DB and Running server
    - git clone https://github.com/JEOO2327/ZOYI_backend.git
    - cd ZOYI_backend
    - python manage.py makemigrations Translation
    - python manage.py migrate
    - python manage.py runserver

- Test Method(Using PostMan)
    - How To Use PostMan
      - POST
        - Select POST METHOD
        - Enter request URL
        - Enter Body(PAYLOAD) : click Body tab -> select raw, JSON(application/json) and enter json data
        - Click Send Button

      - PUT
        - Select PUT Method
        - Enter request URL
        - Enter Body(PAYLOAD) : click Body tab -> select raw, JSON(application/json) and enter json data
        - Click Send Button
  
      - GET
        - Select GET Method
        - Enter request URL
        - Click Send Button

    - request URL : http://localhost:8000/keys
      - POST
        - input examples
          - valid input
            - { "name": "firstkey" } 
            - { "name": "second.key" } 
            - { "name": "third.key.plus.dot." }
          
          - invalid input
            - { "name": "InvAlidKey" }
            - { "name": "invalid_key" }
            - {}

      - GET
        - get example
          - Enter request URL : http://localhost:8000/keys
          - Click Send Button


    - request URL : http://localhost:8000/keys/{keyId}
      - PUT        
        - input examples
          - valid input
            - request URL : http://localhost:8000/keys/1
            - {"name": "modified.first.key"}
          - invalid input
            - request URL : http://localhost:8000/keys/1
            - {"name": "InvalidModify"} 
            
    - request URL : http://localhost:8000/keys/{keyId}/translations/{locale}
      - POST        
        - input examples
          - valid input
            - request URL : http://localhost:8000/keys/1/translations/en
            - {"value": "ship"}
            
            - request URL : http://localhost:8000/keys/1/translations/ko
            - {"value": "배"}

          - invalid input
            - request URL : http://localhost:8000/keys/1/translations/ja
            - {"value": "NotJapanese"} 
      
      - PUT
        - input examples
          - valid input
            - request URL : http://localhost:8000/keys/1/translations/en
            - {"value": "pear"}
            
          - invalid input
            - request URL : http://localhost:8000/keys/1/translations/ko
            - {"value": "NotKorean"} 
      - GET
        - get example
          - Enter request URL : http://localhost:8000/keys/1/translations/ko
          - Click Send Button

               
    - request URL : http://localhost:8000/keys/{keyId}/translations
      - GET
        - get example
          - Enter request URL : http://localhost:8000/keys/1/translations
          - Click Send Button
      
    - request URL : http://localhost:8000/language_detect
      - GET(with Parameter)
        - Select GET Method
        - Enter request URL
        - Enter Parameter :
          - 1'st method : click Params tab -> enter Key(= message) and Value
          - 2'rd method : ADD '?message={value}' To request URL
        - Click Send Button
        
        - input examples
          - valid input
            - Key : message, Value : engish
            - Key : message, Value : 한국어
            - Key : message, Value : にほんご 
          - valid URL
            - http://localhost:8000/language_detect?message=english
            - http://localhost:8000/language_detect?message=한국어
            - http://localhost:8000/language_detect?message=にほんご
            
          - invalid input
            - Key : notmessage, Value : notvalid
            - Key : message, Value : 
          - invalid URL
            - http://localhost:8000/language_detect?notmessage=notvalid
            - http://localhost:8000/language_detect?message=
  
----------------------------------------------------------------------------------------------------------    
 
 - To help understand how to test with POSTMAN, some screen shots are uploaded on the issue that contains a method of entering values and send request using postman.
 
 - Result of input examples are in the issues.
 
 - The Error messages are explained in the issues.
