/******************************************************************************
 *
 * File:        blkocc.h  (Formerly blockocc.h)
 * Description:  Block Occupancy routines
 * Author:       Chris Newton
 * Created:      Fri Nov 8
 * Modified:
 * Language:     C++
 * Package:      N/A
 * Status:       Experimental (Do Not Distribute)
 *
 * (c) Copyright 1991, Hewlett-Packard Company.
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
 ******************************************************************************/

#ifndef           BLKOCC_H
#define           BLKOCC_H

#include                   "varable.h"
#include                   "polyblob.h"
#include          "elst.h"
#include          "notdll.h"
#include          "notdll.h"

/***************************************************************************
CLASS REGION_OCC

  The class REGION_OCC defines a section of outline which exists entirely
  within a single region. The only data held is the min and max x limits of
  the outline within the region.

  REGION_OCCs are held on lists, one list for each region.  The lists are
  built in sorted order of min x. Overlapping REGION_OCCs are not permitted on
  a single list. An overlapping region to be added causes the existing region
  to be extended. This extension may result in the following REGION_OCC on the
  list overlapping the ammended one. In this case the ammended REGION_OCC is
  further extended to include the range of the following one, so that the
  following one can be deleted.

****************************************************************************/

class REGION_OCC:public ELIST_LINK
{
  public:
    float min_x;                 //Lowest x in region
    float max_x;                 //Highest x in region
    INT16 region_type;           //Type of crossing

    REGION_OCC() { 
    };                           //constructor used
    //only in COPIER etc
    REGION_OCC(  //constructor
               float min,
               float max,
               INT16 region) {
      min_x = min;
      max_x = max;
      region_type = region;
    }
};

ELISTIZEH (REGION_OCC)
#define RANGE_IN_BAND( band_max, band_min, range_max, range_min ) \
( ((range_min) >= (band_min)) && ((range_max) < (band_max)) ) ? TRUE : FALSE
/************************************************************************
Adapted from the following procedure so that it can be used in the bands
class in an include file...

BOOL8						range_in_band[
              range within band?
INT16						band_max,
INT16						band_min,
INT16						range_max,
INT16						range_min]
{
  if ( (range_min >= band_min) && (range_max < band_max) )
    return TRUE;
  else
    return FALSE;
}
***********************************************************************/
#define RANGE_OVERLAPS_BAND( band_max, band_min, range_max, range_min ) \
( ((range_max) >= (band_min)) && ((range_min) < (band_max)) ) ? TRUE : FALSE
/************************************************************************
Adapted from the following procedure so that it can be used in the bands
class in an include file...

BOOL8						range_overlaps_band[
              range crosses band?
INT16						band_max,
INT16						band_min,
INT16						range_max,
INT16						range_min]
{
  if ( (range_max >= band_min) && (range_min < band_max) )
    return TRUE;
  else
    return FALSE;
}
***********************************************************************/
/**********************************************************************
  Bands
  -----

  BAND 4
--------------------------------
  BAND 3
--------------------------------

  BAND 2

--------------------------------

  BAND 1

Band 0 is the dot band

Each band has an error margin above and below. An outline is not considered to
have significantly changed bands until it has moved out of the error margin.
*************************************************************************/
class BAND
{
  public:
    INT16 max_max;               //upper max
    INT16 max;                   //nominal max
    INT16 min_max;               //lower max
    INT16 max_min;               //upper min
    INT16 min;                   //nominal min
    INT16 min_min;               //lower min

    BAND() { 
    }                            // constructor

    void set(                      // initialise a band
             INT16 new_max_max,    // upper max
             INT16 new_max,        // new nominal max
             INT16 new_min_max,    // new lower max
             INT16 new_max_min,    // new upper min
             INT16 new_min,        // new nominal min
             INT16 new_min_min) {  // new lower min
      max_max = new_max_max;
      max = new_max;
      min_max = new_min_max;
      max_min = new_max_min;
      min = new_min;
      min_min = new_min_min;
    }

    BOOL8 in_minimal(            //in minimal limits?
                     float y) {  //y value
      if ((y >= max_min) && (y < min_max))
        return TRUE;
      else
        return FALSE;
    }

    BOOL8 in_nominal(            //in nominal limits?
                     float y) {  //y value
      if ((y >= min) && (y < max))
        return TRUE;
      else
        return FALSE;
    }

    BOOL8 in_maximal(            //in maximal limits?
                     float y) {  //y value
      if ((y >= min_min) && (y < max_max))
        return TRUE;
      else
        return FALSE;
    }

                                 //overlaps min limits?
    BOOL8 range_overlaps_minimal(float y1,    //one range limit
                                 float y2) {  //other range limit
      if (y1 > y2)
        return RANGE_OVERLAPS_BAND (min_max, max_min, y1, y2);
      else
        return RANGE_OVERLAPS_BAND (min_max, max_min, y2, y1);
    }

                                 //overlaps nom limits?
    BOOL8 range_overlaps_nominal(float y1,    //one range limit
                                 float y2) {  //other range limit
      if (y1 > y2)
        return RANGE_OVERLAPS_BAND (max, min, y1, y2);
      else
        return RANGE_OVERLAPS_BAND (max, min, y2, y1);
    }

                                 //overlaps max limits?
    BOOL8 range_overlaps_maximal(float y1,    //one range limit
                                 float y2) {  //other range limit
      if (y1 > y2)
        return RANGE_OVERLAPS_BAND (max_max, min_min, y1, y2);
      else
        return RANGE_OVERLAPS_BAND (max_max, min_min, y2, y1);
    }

    BOOL8 range_in_minimal(             //within min limits?
                           float y1,    //one range limit
                           float y2) {  //other range limit
      if (y1 > y2)
        return RANGE_IN_BAND (min_max, max_min, y1, y2);
      else
        return RANGE_IN_BAND (min_max, max_min, y2, y1);
    }

    BOOL8 range_in_nominal(             //within nom limits?
                           float y1,    //one range limit
                           float y2) {  //other range limit
      if (y1 > y2)
        return RANGE_IN_BAND (max, min, y1, y2);
      else
        return RANGE_IN_BAND (max, min, y2, y1);
    }

    BOOL8 range_in_maximal(             //within max limits?
                           float y1,    //one range limit
                           float y2) {  //other range limit
      if (y1 > y2)
        return RANGE_IN_BAND (max_max, min_min, y1, y2);
      else
        return RANGE_IN_BAND (max_max, min_min, y2, y1);
    }
};

/* Standard positions */

#define MAX_NUM_BANDS 5
#define UNDEFINED_BAND 99
#define NO_LOWER_LIMIT -9999
#define NO_UPPER_LIMIT 9999

#define DOT_BAND 0

/* Special occupancy code emitted for the 0 region at the end of a word */

#define END_OF_WERD_CODE 255

extern BOOL_VAR_H (blockocc_show_result, FALSE, "Show intermediate results");
extern INT_VAR_H (blockocc_desc_height, 0,
"Descender height after normalisation");
extern INT_VAR_H (blockocc_asc_height, 255,
"Ascender height after normalisation");
extern INT_VAR_H (blockocc_band_count, 4, "Number of bands used");
extern double_VAR_H (textord_underline_threshold, 0.9,
"Fraction of width occupied");
BOOL8 test_underline(                   //look for underlines
                     BOOL8 testing_on,  //drawing blob
                     PBLOB *blob,       //blob to test
                     float baseline,    //coords of baseline
                     float xheight      //height of line
                    );
BOOL8 test_underline(                   //look for underlines
                     BOOL8 testing_on,  //drawing blob
                     C_BLOB *blob,      //blob to test
                     INT16 baseline,    //coords of baseline
                     INT16 xheight      //height of line
                    );
                                 //project outlines
void horizontal_cblob_projection(C_BLOB *blob,  //blob to project
                                 STATS *stats   //output
                                );
void horizontal_coutline_projection(                     //project outlines
                                    C_OUTLINE *outline,  //outline to project
                                    STATS *stats         //output
                                   );
void set_bands(                 //init from varibles
               float baseline,  //top of bottom band
               float xheight    //height of split band
              );
void block_occ (PBLOB * blob,    //blob to do
float occs[]                     //output histogram
);
                                 //blob to do
void find_transitions(PBLOB *blob, REGION_OCC_LIST *region_occ_list); 
void record_region(  //add region on list
                   INT16 band,
                   float new_min,
                   float new_max,
                   INT16 region_type,
                   REGION_OCC_LIST *region_occ_list);
INT16 find_containing_maximal_band(  //find range's band
                                   float y1,
                                   float y2,
                                   BOOL8 *doubly_contained);
void find_significant_line(POLYPT_IT it, INT16 *band); 
INT16 find_overlapping_minimal_band(  //find range's band
                                    float y1,
                                    float y2);
INT16 find_region_type(INT16 entry_band,
                       INT16 current_band,
                       INT16 exit_band,
                       float entry_x,
                       float exit_x);
void find_trans_point(POLYPT_IT *pt_it,
                      INT16 current_band,
                      INT16 next_band,
                      FCOORD *transition_pt);
void next_region(POLYPT_IT *start_pt_it,
                 INT16 start_band,
                 INT16 *to_band,
                 float *min_x,
                 float *max_x,
                 INT16 *increment,
                 FCOORD *exit_pt);
INT16 find_band(  // find POINT's band
                float y);
void compress_region_list(  // join open regions
                          REGION_OCC_LIST *region_occ_list);
void find_fbox(OUTLINE_IT *out_it,
               float *min_x,
               float *min_y,
               float *max_x,
               float *max_y);
void maintain_limits(float *min_x, float *max_x, float x); 
#endif
