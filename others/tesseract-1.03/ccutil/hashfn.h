/**********************************************************************
 * File:        hashfn.h  (Formerly hash.h)
 * Description: Simple hash function.
 * Author:					Ray Smith
 * Created:					Thu Jan 16 11:47:59 GMT 1992
 *
 * (C) Copyright 1992, Hewlett-Packard Ltd.
 ** Licensed under the Apache License, Version 2.0 (the "License");
 ** you may not use this file except in compliance with the License.
 ** You may obtain a copy of the License at
 ** http://www.apache.org/licenses/LICENSE-2.0
 ** Unless required by applicable law or agreed to in writing, software
 ** distributed under the License is distributed on an "AS IS" BASIS,
 ** WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 ** See the License for the specific language governing permissions and
 ** limitations under the License.
 *
 **********************************************************************/

#ifndef           HASHFN_H
#define           HASHFN_H

#include          "host.h"

INT32 hash(               //hash function
           INT32 bits,    //bits in hash function
           void *key,     //key to hash
           INT32 keysize  //size of key
          );
#endif
