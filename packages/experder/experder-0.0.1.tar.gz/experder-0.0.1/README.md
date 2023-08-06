# experder
### a caesar cypher library and 10-key encryption lilbrary for python

## Download
`python3 -m pip install experder`  
or   
`pip install experder`  

## Usage

- caesar_rshift
shifts each character by `key`
```python3
caesar_rshift(message, key=13)

caesar_rshift('lcpmatthew@gmail.com')
>> 'ypcznggurj@tznvy.pbz'

# Also works with upper and lower case
caesar_rshift('lcpmatthew@gmail.COM', 25)
>> 'kbolzssgdv@flzhk.BNL'
```

- caesar_lshift
shifts each character backwards by `key`
```python3
caesar_lshift(message, key=13)

caesar_lshift('ypcznggurj@tznvy.pbz')
>> 'lcpmatthew@gmail.com'

caesar_lshift('kbolzssgdv@flzhk.BNL', 25)    
>> 'lcpmatthew@gmail.COM'
```

- caesar_bruteforce
checks every possible combination for caesar encryption and prints on screen
```python3
caesar_bruteforce(message)

caesar_bruteforce('kbolzssgdv@flzhk.BNL')
>>  0|kbolzssgdv@flzhk.BNL
>>  1|jankyrrfcu@ekygj.AMK
>>  2|izmjxqqebt@djxfi.ZLJ
>>  3|hyliwppdas@ciweh.YKI
>>  4|gxkhvooczr@bhvdg.XJH
>>  5|fwjgunnbyq@agucf.WIG
>>  6|eviftmmaxp@zftbe.VHF
>>  7|duhesllzwo@yesad.UGE
>>  8|ctgdrkkyvn@xdrzc.TFD
>>  9|bsfcqjjxum@wcqyb.SEC
>> 10|arebpiiwtl@vbpxa.RDB
>> 11|zqdaohhvsk@uaowz.QCA
>> 12|ypcznggurj@tznvy.PBZ
>> 13|xobymfftqi@symux.OAY
>> 14|wnaxleesph@rxltw.NZX
>> 15|vmzwkddrog@qwksv.MYW
>> 16|ulyvjccqnf@pvjru.LXV
>> 17|tkxuibbpme@ouiqt.KWU
>> 18|sjwthaaold@nthps.JVT
>> 19|rivsgzznkc@msgor.IUS
>> 20|qhurfyymjb@lrfnq.HTR
>> 21|pgtqexxlia@kqemp.GSQ
>> 22|ofspdwwkhz@jpdlo.FRP
>> 23|nerocvvjgy@iockn.EQO
>> 24|mdqnbuuifx@hnbjm.DPN
>> 25|lcpmatthew@gmail.COM
```

- tenkey_rshift
Does not only have to be ten key  
Works like this:  

`tenkey_rshift('aaaa',15)`
| a | a | a |a|
|:--:|:--:|:--:|  :--:|
| 1 | 5 | 1 | 5
|b|f|b|f

`tenkey_rshift('aaaa',153)`
| a | a | a |a|
|:--:|:--:|:--:|  :--:|
| 1 | 5 | 3 | 1
|b|f|d|b

`tenkey_rshift('aa aa',153, skip_spaces=True)`
| a | a | | a |a
|:--:|:--:|:--:|  :--:|:--: |
| 1 | 5 | \ | 3 | 1
|b|f| | 3 | 1

`tenkey_rshift('aa aa',153, skip_spaces=False)`
| a | a | | a |a
|:--:|:--:|:--:|  :--:|:--: |
| 1 | 5 | 3| 1 | 5
|b|f|  | b | f

```python3
tenkey_rshift(message, key, skip_spaces=True)
```

- tenkey_lshift
works like tenkey_rshift but shifts left


###### experder
###### Matthew Lam 2020