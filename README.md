# TTS-norm-service
TTS-norm-service is an api for converting text from written form into spoken form.


TTS norm service composes of 4 parts:

**Input**: sample in the form of written form

**Output**: sample in the form of spoken form

     ex: hôm nay là ngày 20/10 --> hôm nay là ngày hai mươi tháng mười

**Norm by dictionary:**
 
* abbreviation dictionary in the format: `[abbre form] <tab> [spoken form]`
* replace abbreviation word from abbreviation dictionary: `VN --> Việt Nam`

**Norm by RULE**

We use Regex to classify non-standard words and then generate full words for them:
 
- DATE: `1/1/2020 --> Ngày mùng một tháng một năm hai nghìn không trăm hai mươi`  
- TIME: `8h30 --> tám giờ ba mươi`  
- MEASURE: `5km --> năm ki lô mét`  
- FRACTION: `3/4 --> ba phần bốn` 
- SCORE: `tỉ số 3-0 --> tỉ số ba không` 
- DIGIT: `0969696969 --> không chín sáu chín sáu chín sáu chín sáu chín`  
- ROMAN: `XV --> mười lăm`  
- DECIMAL: `2,4 --> hai phẩy bốn`  
- CARDINAL: `6 --> sáu`  



**NOTES:** all punctuation excluding comma, period, exclamation, question will be replaced by comma.






##Usage

Run api: `python service.py`

- Get the name of server and test with Postman application  
- Using normal norm service, from text to text: Request to host:port/norm
- Send GET/POST request using raw JSON with 2 arguments: "sample" and "text"
- Text normalized will return in the response  

Run file:
```
   python norm_file.py [input_file] [output_file]
```