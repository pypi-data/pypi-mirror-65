json
====

.. automodule:: parce.lang.json
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Json.root`` and text:

.. code-block:: json

    {
      "title": "Frescobaldi",
      "background": "background.png",
      "icon-size": 80,
      "contents": [
        { "x": 449, "y": 320, "type": "link", "path": "/Applications"},
        { "x": 188, "y": 320, "type": "file", "path": "../dist/Frescobaldi.app"},
        { "x": 100, "y": 70, "type": "file", "path": "../README.txt" },
        { "x": 100, "y": 185, "type": "file", "path": "../ChangeLog.txt" },
        { "x": 540, "y": 70, "type": "file", "path": "../COPYING.txt" }
      ]
    }

Result tree::

    <Context Json.root at 0-456 (2 children)>
     ├╴<Token '{' at 0:1 (Delimiter)>
     ╰╴<Context Json.object at 4-456 (8 children)>
        ├╴<Context Json.key at 4-12 (3 children)>
        │  ├╴<Token '"' at 4:5 (Literal.String)>
        │  ├╴<Context Json.string at 5-11 (2 children)>
        │  │  ├╴<Token 'title' at 5:10 (Literal.String)>
        │  │  ╰╴<Token '"' at 10:11 (Literal.String)>
        │  ╰╴<Token ':' at 11:12 (Delimiter)>
        ├╴<Context Json.value at 13-27 (3 children)>
        │  ├╴<Token '"' at 13:14 (Literal.String)>
        │  ├╴<Context Json.string at 14-26 (2 children)>
        │  │  ├╴<Token 'Frescobaldi' at 14:25 (Literal.String)>
        │  │  ╰╴<Token '"' at 25:26 (Literal.String)>
        │  ╰╴<Token ',' at 26:27 (Delimiter)>
        ├╴<Context Json.key at 30-43 (3 children)>
        │  ├╴<Token '"' at 30:31 (Literal.String)>
        │  ├╴<Context Json.string at 31-42 (2 children)>
        │  │  ├╴<Token 'background' at 31:41 (Literal.String)>
        │  │  ╰╴<Token '"' at 41:42 (Literal.String)>
        │  ╰╴<Token ':' at 42:43 (Delimiter)>
        ├╴<Context Json.value at 44-61 (3 children)>
        │  ├╴<Token '"' at 44:45 (Literal.String)>
        │  ├╴<Context Json.string at 45-60 (2 children)>
        │  │  ├╴<Token 'background.png' at 45:59 (Literal.String)>
        │  │  ╰╴<Token '"' at 59:60 (Literal.String)>
        │  ╰╴<Token ',' at 60:61 (Delimiter)>
        ├╴<Context Json.key at 64-76 (3 children)>
        │  ├╴<Token '"' at 64:65 (Literal.String)>
        │  ├╴<Context Json.string at 65-75 (2 children)>
        │  │  ├╴<Token 'icon-size' at 65:74 (Literal.String)>
        │  │  ╰╴<Token '"' at 74:75 (Literal.String)>
        │  ╰╴<Token ':' at 75:76 (Delimiter)>
        ├╴<Context Json.value at 77-80 (2 children)>
        │  ├╴<Token '80' at 77:79 (Literal.Number)>
        │  ╰╴<Token ',' at 79:80 (Delimiter)>
        ├╴<Context Json.key at 83-94 (3 children)>
        │  ├╴<Token '"' at 83:84 (Literal.String)>
        │  ├╴<Context Json.string at 84-93 (2 children)>
        │  │  ├╴<Token 'contents' at 84:92 (Literal.String)>
        │  │  ╰╴<Token '"' at 92:93 (Literal.String)>
        │  ╰╴<Token ':' at 93:94 (Delimiter)>
        ╰╴<Context Json.value at 95-456 (3 children)>
           ├╴<Token '[' at 95:96 (Delimiter)>
           ├╴<Context Json.array at 101-454 (15 children)>
           │  ├╴<Token '{' at 101:102 (Delimiter)>
           │  ├╴<Context Json.object at 103-163 (8 children)>
           │  │  ├╴<Context Json.key at 103-107 (3 children)>
           │  │  │  ├╴<Token '"' at 103:104 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 104-106 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 104:105 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 105:106 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 106:107 (Delimiter)>
           │  │  ├╴<Context Json.value at 108-112 (2 children)>
           │  │  │  ├╴<Token '449' at 108:111 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 111:112 (Delimiter)>
           │  │  ├╴<Context Json.key at 113-117 (3 children)>
           │  │  │  ├╴<Token '"' at 113:114 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 114-116 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 114:115 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 115:116 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 116:117 (Delimiter)>
           │  │  ├╴<Context Json.value at 118-122 (2 children)>
           │  │  │  ├╴<Token '320' at 118:121 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 121:122 (Delimiter)>
           │  │  ├╴<Context Json.key at 123-130 (3 children)>
           │  │  │  ├╴<Token '"' at 123:124 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 124-129 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 124:128 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 128:129 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 129:130 (Delimiter)>
           │  │  ├╴<Context Json.value at 131-138 (3 children)>
           │  │  │  ├╴<Token '"' at 131:132 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 132-137 (2 children)>
           │  │  │  │  ├╴<Token 'link' at 132:136 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 136:137 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 137:138 (Delimiter)>
           │  │  ├╴<Context Json.key at 139-146 (3 children)>
           │  │  │  ├╴<Token '"' at 139:140 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 140-145 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 140:144 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 144:145 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 145:146 (Delimiter)>
           │  │  ╰╴<Context Json.value at 147-163 (3 children)>
           │  │     ├╴<Token '"' at 147:148 (Literal.String)>
           │  │     ├╴<Context Json.string at 148-162 (2 children)>
           │  │     │  ├╴<Token '/Applications' at 148:161 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 161:162 (Literal.String)>
           │  │     ╰╴<Token '}' at 162:163 (Delimiter)>
           │  ├╴<Token ',' at 163:164 (Delimiter)>
           │  ├╴<Token '{' at 169:170 (Delimiter)>
           │  ├╴<Context Json.object at 171-241 (8 children)>
           │  │  ├╴<Context Json.key at 171-175 (3 children)>
           │  │  │  ├╴<Token '"' at 171:172 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 172-174 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 172:173 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 173:174 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 174:175 (Delimiter)>
           │  │  ├╴<Context Json.value at 176-180 (2 children)>
           │  │  │  ├╴<Token '188' at 176:179 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 179:180 (Delimiter)>
           │  │  ├╴<Context Json.key at 181-185 (3 children)>
           │  │  │  ├╴<Token '"' at 181:182 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 182-184 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 182:183 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 183:184 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 184:185 (Delimiter)>
           │  │  ├╴<Context Json.value at 186-190 (2 children)>
           │  │  │  ├╴<Token '320' at 186:189 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 189:190 (Delimiter)>
           │  │  ├╴<Context Json.key at 191-198 (3 children)>
           │  │  │  ├╴<Token '"' at 191:192 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 192-197 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 192:196 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 196:197 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 197:198 (Delimiter)>
           │  │  ├╴<Context Json.value at 199-206 (3 children)>
           │  │  │  ├╴<Token '"' at 199:200 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 200-205 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 200:204 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 204:205 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 205:206 (Delimiter)>
           │  │  ├╴<Context Json.key at 207-214 (3 children)>
           │  │  │  ├╴<Token '"' at 207:208 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 208-213 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 208:212 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 212:213 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 213:214 (Delimiter)>
           │  │  ╰╴<Context Json.value at 215-241 (3 children)>
           │  │     ├╴<Token '"' at 215:216 (Literal.String)>
           │  │     ├╴<Context Json.string at 216-240 (2 children)>
           │  │     │  ├╴<Token '../dist/Frescobaldi.app' at 216:239 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 239:240 (Literal.String)>
           │  │     ╰╴<Token '}' at 240:241 (Delimiter)>
           │  ├╴<Token ',' at 241:242 (Delimiter)>
           │  ├╴<Token '{' at 247:248 (Delimiter)>
           │  ├╴<Context Json.object at 249-309 (8 children)>
           │  │  ├╴<Context Json.key at 249-253 (3 children)>
           │  │  │  ├╴<Token '"' at 249:250 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 250-252 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 250:251 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 251:252 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 252:253 (Delimiter)>
           │  │  ├╴<Context Json.value at 254-258 (2 children)>
           │  │  │  ├╴<Token '100' at 254:257 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 257:258 (Delimiter)>
           │  │  ├╴<Context Json.key at 259-263 (3 children)>
           │  │  │  ├╴<Token '"' at 259:260 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 260-262 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 260:261 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 261:262 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 262:263 (Delimiter)>
           │  │  ├╴<Context Json.value at 264-267 (2 children)>
           │  │  │  ├╴<Token '70' at 264:266 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 266:267 (Delimiter)>
           │  │  ├╴<Context Json.key at 268-275 (3 children)>
           │  │  │  ├╴<Token '"' at 268:269 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 269-274 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 269:273 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 273:274 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 274:275 (Delimiter)>
           │  │  ├╴<Context Json.value at 276-283 (3 children)>
           │  │  │  ├╴<Token '"' at 276:277 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 277-282 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 277:281 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 281:282 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 282:283 (Delimiter)>
           │  │  ├╴<Context Json.key at 284-291 (3 children)>
           │  │  │  ├╴<Token '"' at 284:285 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 285-290 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 285:289 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 289:290 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 290:291 (Delimiter)>
           │  │  ╰╴<Context Json.value at 292-309 (3 children)>
           │  │     ├╴<Token '"' at 292:293 (Literal.String)>
           │  │     ├╴<Context Json.string at 293-307 (2 children)>
           │  │     │  ├╴<Token '../README.txt' at 293:306 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 306:307 (Literal.String)>
           │  │     ╰╴<Token '}' at 308:309 (Delimiter)>
           │  ├╴<Token ',' at 309:310 (Delimiter)>
           │  ├╴<Token '{' at 315:316 (Delimiter)>
           │  ├╴<Context Json.object at 317-381 (8 children)>
           │  │  ├╴<Context Json.key at 317-321 (3 children)>
           │  │  │  ├╴<Token '"' at 317:318 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 318-320 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 318:319 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 319:320 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 320:321 (Delimiter)>
           │  │  ├╴<Context Json.value at 322-326 (2 children)>
           │  │  │  ├╴<Token '100' at 322:325 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 325:326 (Delimiter)>
           │  │  ├╴<Context Json.key at 327-331 (3 children)>
           │  │  │  ├╴<Token '"' at 327:328 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 328-330 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 328:329 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 329:330 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 330:331 (Delimiter)>
           │  │  ├╴<Context Json.value at 332-336 (2 children)>
           │  │  │  ├╴<Token '185' at 332:335 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 335:336 (Delimiter)>
           │  │  ├╴<Context Json.key at 337-344 (3 children)>
           │  │  │  ├╴<Token '"' at 337:338 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 338-343 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 338:342 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 342:343 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 343:344 (Delimiter)>
           │  │  ├╴<Context Json.value at 345-352 (3 children)>
           │  │  │  ├╴<Token '"' at 345:346 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 346-351 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 346:350 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 350:351 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 351:352 (Delimiter)>
           │  │  ├╴<Context Json.key at 353-360 (3 children)>
           │  │  │  ├╴<Token '"' at 353:354 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 354-359 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 354:358 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 358:359 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 359:360 (Delimiter)>
           │  │  ╰╴<Context Json.value at 361-381 (3 children)>
           │  │     ├╴<Token '"' at 361:362 (Literal.String)>
           │  │     ├╴<Context Json.string at 362-379 (2 children)>
           │  │     │  ├╴<Token '../ChangeLog.txt' at 362:378 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 378:379 (Literal.String)>
           │  │     ╰╴<Token '}' at 380:381 (Delimiter)>
           │  ├╴<Token ',' at 381:382 (Delimiter)>
           │  ├╴<Token '{' at 387:388 (Delimiter)>
           │  ├╴<Context Json.object at 389-450 (8 children)>
           │  │  ├╴<Context Json.key at 389-393 (3 children)>
           │  │  │  ├╴<Token '"' at 389:390 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 390-392 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 390:391 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 391:392 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 392:393 (Delimiter)>
           │  │  ├╴<Context Json.value at 394-398 (2 children)>
           │  │  │  ├╴<Token '540' at 394:397 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 397:398 (Delimiter)>
           │  │  ├╴<Context Json.key at 399-403 (3 children)>
           │  │  │  ├╴<Token '"' at 399:400 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 400-402 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 400:401 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 401:402 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 402:403 (Delimiter)>
           │  │  ├╴<Context Json.value at 404-407 (2 children)>
           │  │  │  ├╴<Token '70' at 404:406 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 406:407 (Delimiter)>
           │  │  ├╴<Context Json.key at 408-415 (3 children)>
           │  │  │  ├╴<Token '"' at 408:409 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 409-414 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 409:413 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 413:414 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 414:415 (Delimiter)>
           │  │  ├╴<Context Json.value at 416-423 (3 children)>
           │  │  │  ├╴<Token '"' at 416:417 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 417-422 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 417:421 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 421:422 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 422:423 (Delimiter)>
           │  │  ├╴<Context Json.key at 424-431 (3 children)>
           │  │  │  ├╴<Token '"' at 424:425 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 425-430 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 425:429 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 429:430 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 430:431 (Delimiter)>
           │  │  ╰╴<Context Json.value at 432-450 (3 children)>
           │  │     ├╴<Token '"' at 432:433 (Literal.String)>
           │  │     ├╴<Context Json.string at 433-448 (2 children)>
           │  │     │  ├╴<Token '../COPYING.txt' at 433:447 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 447:448 (Literal.String)>
           │  │     ╰╴<Token '}' at 449:450 (Delimiter)>
           │  ╰╴<Token ']' at 453:454 (Delimiter)>
           ╰╴<Token '}' at 455:456 (Delimiter)>


