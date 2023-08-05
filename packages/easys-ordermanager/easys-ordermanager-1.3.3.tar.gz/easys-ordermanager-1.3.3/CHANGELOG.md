# Changelog

## 1.3.2 (2020-04-02)
Added new OrdeLine Serializer for Landingpage product `OrderLineLandingpageSerializer`. 
(The fields definitions of the Landingpage order line are the same as those from the `OrderLineWebsiteSerializer`)
  * `additional_subpages`: mandatory positive integer
  * `logo_creation`: 3 choices field:
    * 1: 'Create new logo'
    * 2: 'Use existing logo'
    * 3: 'No logo at all, text only'

Changes on `OrderLineSerializer`
  * Add new field `detail_landingpage` of type `OrderLineLandingpageSerializer`

Changes on `OrderLineGoogleAdsBasicSerializer`
  * Add  `target_page_type` field which accepts 3 choices (see `GOOGLE_ADS_LANDING_PAGE_CHOICES`): 
    * 1: 'New website'
    * 2: 'Customer website'
    * 3: 'New landingpage'
    
Changes on `OrderLineGoogleAdsPremiumSerializer`
  * Add `branch_codes` field which accepts a list of Herocentral equivalent of an Industry Topic codes. Herocentral will validate their existence.
  * Add  `target_page_type` field which accepts 3 choices (see `GOOGLE_ADS_LANDING_PAGE_CHOICES`): 
    * 'new': 'New website'
    * 'new_lp': 'New landingpage'
    * 'customer': 'Customer website'
  * Add Decimal field `remarketing_setup_fee`. Validate that value >=0 is provided if `include_remarketing=true` 
  * Add Decimal field `remarketing_budget`. Validate that that value >0 is provided if `include_remarketing=true`

Add new validation on the main Serializer: If a product provides value for `target_page_type` and that value is a website or a landingpage choice, validate that the main order contains an order for website or landingpage product.


## 1.2.3 (2020-03-03)
Make sure Django 3 is not installed until further support

## 1.2.2 (2020-03-03)
Add proper dependencies to avoid unwanted failure with possible upgrades when installed freshly.
See requirements.txt for dependencies

## 1.2.1 (2020-02-27)
Add unique validation on `opening_hours` list of values of `OrderLineListingSerializer`. 
The  opening hours lis should be unique for every `day_of_week` (see `OrderLineListingOpeningHoursSerializer`)


## 1.2.0 (2019-09-17)
This release contains backwards incompatible changes.

Changes on `OrderLineDisplayBasicSerializer`   
  * Removed: `geo_targeting` field.
  * New: `geo_targeting_zip` field which accepts one string zip code. Not mandatory
  * New: `geo_targeting_radius` field accepting integer values between 1-80 (km). Mandatory only if `geo_targeting_zip` is given.  
  * Removed: `stock_images_allowed` field:
  * New: `banner_image_selection` choice field accepting following values: 
    * 0 for 'From website' / 'Von der Webseite' option
    * 1 for 'From customer' / 'Vom kunden' option
    * 2 for 'Customer photos' / 'Regiohelden Bilder' option 
  * Change: `target_page_type` existing field which is not required anymore.

Changes on `OrderLineGoogleAdsPremiumSerializer`:
  * New: `call_tracking` boolean required field.
  

## 1.1.3 (2019-09-11)
Clean README file.


## 1.1.2 (2019-09-11)
Fix expected_impression_share field of OrderLineGoogleAdsBasicSerializer to accept 5 digits in order to validate value 100.00


## 1.1.1 (2019-09-06)
Small fix on pep8 error

## 1.1.0 (2019-09-04)

This release contains backwards incompatible changes


* Split Display detail OrderLineDisplaySerializer in two different serializers and fields for basic and premium product levels:
  * remove `detail_display` field from `OrderLine` 
  * add `detail_display_basic` field (`OrderLineDisplayBasicSerializer`) on `OrderLine`  
   
     The serializer contains following fields:  
     
     New fields:
       * `banner_color_selection`  
         choice field with values: 1 for _Color from Logo/Website_ and 2 for _Set color_ . To be used in combination with fields `color_code_x`  
     
     Fields with changed definition
       * `impressions_per_month`  
         choice field with accepted values: 20.000 , 40.000 and 80.000
       * `creative_options`  
         choice field contains only values: 1 for _Customer provided_ and 3 for _Create animated_
     
     Fields with the same definition as in the previous OrderLineDisplaySerializer
       * `geo_targeting`
       * `geo_targeting`
       * `campaign_goal`
       * `headline`
       * `sub_headline`
       * `bullet_points`
       * `call_to_action`
       * `color_code_1`
       * `color_code_2`
       * `color_code_3`
       * `stock_images_allowed`
       * `target_page_type`
       * `target_url`
       * `package_template`
       * `location_frame_text`
       * `creative_options`
      
  * add `detail_display_premium` field (`OrderLineDisplayPremiumSerializer`) on `OrderLine`   
   
     Serializer contains following fields with the same definition as in the previous OrderLineDisplaySerializer
       * `booking_type`
       * `target_devices`
       * `creatives_format`
       * `impressions_per_day`
       * `impressions_per_month`
       * `age_targeting`
       * `gender_targeting`
       * `geo_targeting`
       * `channel_targeting`
       * `interest_targeting`
       * `campaign_goal`
       * `target_page_type`
       * `target_url`
       * `creative_options`
      

* Split Google Ads detail OrderLineGoogleAdsSerializer in two different serializers for basic and premium product levels:
  * remove `detail_google_ads` field from `OrderLine`     
  * add `detail_google_ads_basic` field (`OrderLineGoogleAdsBasicSerializer`) on `OrderLine`  

       Serializer contains following fields with the same definition as in the previous OrderLineGoogleAdsSerializer
    * `campaign_goal`
    * `regions`
    * `expected_impression_share`
    * `keywords`
    * `keywords_with_zero_search_volume`
    * `target_audience`

  * add `detail_google_ads_premium` field (`OrderLineGoogleAdsPremiumSerializer`) on `OrderLine`  

       Serializer contains following fields with the same definition as in the previous OrderLineGoogleAdsSerializer
     * `call_to_action`
     * `campaign_goal`
     * `regions`
     * `expected_clicks`
     * `expected_conversions`
     * `existing_account_id`
     * `include_remarketing`
     * `keywords`
     * `keywords_with_zero_search_volume`
     * `target_audience`
     * `usp`


* All product fee fields on `OrderLineSerializer` became optional:
  * `setup_fee`
  * `start_fee`
  * `budget`
  * `fee`
  * `one_time_budget`
  * `commission`
  * `deferred_payment_sum`

* Add validation for commission provided for product type Google Ads level Basic: fixed value of 40  
* Add validation for combination of product type and level: check if a matching HC products subtype exists
* Add validation for the payment fees provided: check if a matching HC payment type exists.


## 1.0.4 (2019-08-21)

* Add new fee type postponed_setup_fee
* Add reference customer boolean to Location serializer

## 1.0.3 (2019-07-03)

* Don't use allow_null with BooleanField (`djangorestframework<3.9` doesn't support it)


## 1.0.2 (2019-07-01)

* Allow to use empty/null values for non-required fields


## 1.0.1 (2019-06-27)

* Add missing files to the package


## 1.0.0 (2019-06-24)

* Initial release
