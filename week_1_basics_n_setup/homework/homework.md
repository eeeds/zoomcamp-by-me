## Week 1 Homework

In this homework we'll prepare the environment 
and practice with terraform and SQL


## Question 1. Google Cloud SDK

Install Google Cloud SDK. What's the version you have? 

To get the version, run `gcloud --version`
## Answer:
```
Google Cloud SDK 383.0.1
bq 2.0.74      
core 2022.04.26
gsutil 5.9
```


## Google Cloud account 

Create an account in Google Cloud and create a project.


## Question 2. Terraform 

Now install terraform and go to the terraform directory (`week_1_basics_n_setup/1_terraform_gcp/terraform`)

After that, run

* `terraform init`
* `terraform plan`
* `terraform apply` 

Apply the plan and copy the output (after running `apply`) to the form.

It should be the entire output - from the moment you typed `terraform init` to the very end.

## Prepare Postgres 

Run Postgres and load data as shown in the videos

We'll use the yellow taxi trips from January 2021:

```bash
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```

You will also need the dataset with zones:

```bash 
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Download this data and put it to Postgres

## Question 3. Count records 

How many taxi trips were there on January 15?

Consider only trips that started on January 15.
## Answer:
```
SELECT COUNT(*) FROM yellow_taxi_trips WHERE pickup_datetime LIKE '%15-01-%';
```


## Question 4. Largest tip for each day

Find the largest tip for each day. 
On which day it was the largest tip in January?

Use the pick up time for your calculations.

(note: it's not a typo, it's "tip", not "trip")
## Answer:
```
select tpep_pickup_datetime, max(tip_amount)
from yellow_taxi_trip
where extract(month from tpep_pickup_datetime) = 01
group by tpep_pickup_datetime
order by max(tip_amount) desc;
```


## Question 5. Most popular destination

What was the most popular destination for passengers picked up 
in central park on January 14?

Use the pick up time for your calculations.
Enter the zone name (not id). If the zone name is unknown (missing), write "Unknown" 
## Answer:
```
select coalesce(zod."Zone", 'Unknown'), count(*)
from 
yellow_taxi_trip t,
zones zup,
zones zod
where t."PULocationID"=zup."LocationID"
and t."DOLocationID"= zod."LocationID"
and extract(month from t."tpep_pickup_datetime")=01
and extract(day from t."tpep_pickup_datetime")= 14
and zup."Zone" like '%Central Park%'
group by zod."Zone"
order by count(*) desc 
limit 1;
```


## Question 6. Most expensive locations

What's the pickup-dropoff pair with the largest 
average price for a ride (calculated based on `total_amount`)?

Enter two zone names separated by a slash

For example:

"Jamaica Bay / Clinton East"

If any of the zone names are unknown (missing), write "Unknown". For example, "Unknown / Clinton East". 
## Answer:
```
select concat(coalesce(zup."Zone", 'Unknown')  ,'/',coalesce(zod."Zone", 'Unknown')),t.total_amount
from 
yellow_taxi_trip t,
zones zup,
zones zod
where t."PULocationID"=zup."LocationID"
and t."DOLocationID"= zod."LocationID"
order by t.total_amount desc 
limit 1;
```

## Submitting the solutions

* Form for submitting: https://forms.gle/yGQrkgRdVbiFs8Vd7
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Wednesday), 22:00 CET


## Solution

Here is the solution to questions 3-6: [video](https://www.youtube.com/watch?v=HxHqH2ARfxM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
