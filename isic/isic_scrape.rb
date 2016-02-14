require 'open-uri'
require 'json'

def retrieve_as_json(url)
  JSON.parse(retrieve_data(url))
end

def retrieve_data(url)
  open(url).read
end

def get_datasets
  dataset_url = 'https://isic-archive.com:443/api/v1/dataset?limit=50&offset=0&sort=lowerName&sortdir=1'
  retrieve_as_json(dataset_url)
end

puts "Starting image scrape."

datasets = get_datasets

puts "Found #{datasets.count} datasets."

def get_list_of_images(dataset_id)
  pattern = -> (id) { "https://isic-archive.com:443/api/v1/image?limit=1000000&offset=0&sort=lowerName&sortdir=1&datasetId=#{id}" }
  retrieve_as_json(pattern.call(dataset_id))
end

list_of_images = []

datasets.each do |d|
  list_of_images += get_list_of_images(d['_id'])
end

require 'json'

def get_metadata(image_id)
  pattern = -> (id) { "https://isic-archive.com:443/api/v1/image/#{id}" }
  retrieve_as_json(pattern.call(image_id))
end

ground_truth = File.open('isic_ground_truth.csv', 'w')

list_of_images.each_with_index do |image, indx|
  puts "Retrieving image #{indx} in result set."

  image_id = image['_id']

  metadata = get_metadata(image_id)
  clinical_metadata = metadata['meta']['clinical']

  metadata_file = "./isic_metadata/#{image_id}"
  File.open(metadata_file, 'w') { |f| f.write(clinical_metadata.to_json) }
  puts "Wrote metadata to file - #{metadata_file}."

  res = ['ben_mal', 'benign_malignant', 'malignant'].any? do |possible_key|
    if (result = clinical_metadata[possible_key])
      ground_truth.puts("#{image_id},#{result}")
      puts "Wrote class #{result} to file for #{image_id}."

      true
    else
      false
    end
  end

  raise "Image #{image_id} did not contain one of the required keys." if !res

  sleep(0.01)
end

ground_truth.close

puts list_of_images.count

def download_image(image_id)
  pattern = -> (id) { "https://isic-archive.com:443/api/v1/image/#{id}/download" }
  retrieve_data(pattern.call(image_id))
end

batched_list = list_of_images.each_slice(339).to_a

threads = batched_list.map do |list|
  Thread.new(list) do |list|
    list.each_with_index do |image, indx|
      puts "Retrieving image #{indx} in result set."

      image_id = image['_id']

      image_file = "./isic_images/#{image_id}"

      begin
        File.open(image_file, 'wb') { |f| f.write(download_image(image_id)) }
        # puts "Wrote image to file - #{image_file}."
      rescue
        puts "Failed to grab #{image_id}."
        next
      end

      sleep(0.01)
    end
  end
end

threads.each { |t| t.join }
