require 'geokit'
require 'csv'
require 'fastest-csv'
require 'active_record'
require 'activerecord-import'

Geokit::default_units = :meters

ActiveRecord::Base.establish_connection(
  :adapter  => 'postgresql',
  :database => 'highroads',
  :host     => 'localhost'
)

class RoadSegment < ActiveRecord::Base
  def self.calculate_intermediate_coordinates(start_lat_lng,end_lat_lng)
    coord_set = []
    a = Geokit::LatLng.new(start_lat_lng[0],start_lat_lng[1])
    b = Geokit::LatLng.new(end_lat_lng[0],end_lat_lng[1])

    distance =  a.distance_to(b)
    heading = a.heading_to(b)

    stops = (distance/10).ceil
    stop_distance = distance/stops
    (stops - 1).times do |x|
      coord_set << a.endpoint(heading, (x + 1) * stop_distance)
    end
    coord_set << b
    coord_set
  end

  def self.import_csv(file_name)
    line_count = CSV.read("#{file_name}").count
    x = 0
    road_segments = []
    last_row = []
    CSV.open("#{file_name.split(".")[0]}_result2.csv","w") do |csv|
    FastestCSV.foreach("#{file_name}") do |row|
      if row[0] == last_row[0] && ["S1100","S1200","S1400"].include?(row[3])
        coords = calculate_intermediate_coordinates([last_row[4],last_row[5]],[row[4],row[5]])
        coords.each do |coord|
          csv << [row[0],row[1],row[2],row[3],coord.lat,coord.lng]
=begin
          road_segments << RoadSegment.new(
            state_code: state_code,
            linearid: row[0],
            fullname: row[1],
            rttyp: row[2],
            mtfcc: row[3],
            lat: coord.lat,
            lng: coord.lng
          )
=end
        end
      elsif ["S1100","S1200","S1400"].include?(row[3])
      #else
        csv << row
=begin

        road_segments << RoadSegment.new(
          state_code: state_code,
          linearid: row[0],
          fullname: row[1],
          rttyp: row[2],
          mtfcc: row[3],
          lat: row[4],
          lng: row[5]
        )
=end
      end
      last_row = row
      x += 1
      print "#{x}/#{line_count} \r"
    end
    end
    puts "co-ordinate building finished, importing"
    #RoadSegment.import road_segments
  end

end

RoadSegment.import_csv("roads_csvs/02_Alaska.csv")
