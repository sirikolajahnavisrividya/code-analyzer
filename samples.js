export const LANGS = {
 python:["Python","py","python"], javascript:["JavaScript","js","javascript"], typescript:["TypeScript","ts","typescript"], java:["Java","java","java"],
 c:["C","c","c"], cpp:["C++","cpp","cpp"], csharp:["C#","cs","csharp"], go:["Go","go","go"], rust:["Rust","rs","rust"], php:["PHP","php","php"],
 ruby:["Ruby","rb","ruby"], kotlin:["Kotlin","kt","kotlin"], swift:["Swift","swift","swift"], sql:["SQL","sql","sql"]};
export const SAMPLES = {
python:`import hashlib, sqlite3
password = "admin123"
def find(username, items, other):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    try:
        result = [a for a in items for b in other if a == b]
    except:
        pass
    return hashlib.md5(password.encode()).hexdigest(), result
print("Result:", find("bob", [1,2,3], [2,3])[1])
`,
javascript:`var apiKey = "sk-12345";
function show(name) {
  document.body.innerHTML = "<h1>" + name + "</h1>";
}
console.log("Hello from JS", eval("1+2"));
`,
c:`#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main() {
  char buf[8];
  char *p = malloc(10);
  strcpy(buf, "hi");
  printf("Hello %s\\n", buf);
  return 0;
}
`,
sql:`-- TODO: add index
SELECT * FROM users;
DELETE FROM orders;
`};
export const sampleFor = l => SAMPLES[l] || `// Sample for ${l}: write your code here\n`;
export const fileName = l => (l==="java"?"YourCode.java":l==="sql"?"your_code.sql":`your_code.${LANGS[l][1]}`);
