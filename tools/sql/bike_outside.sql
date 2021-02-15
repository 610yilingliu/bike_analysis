--0 : bike inside fence, 1: bike outside fence
select * from cleaned_bike_required where IS_INSIDE = 0;
select * from cleaned_bike_required where IS_INSIDE = 1;