const accommodationKeys = [
    "accommodation_name",
      "accommodation_description",
      "injury_location_name",
      "industry_name",
      "activity_name",
      "verified",
      "date_created"
]

const headers = [
    'Accommodation',
    'Part of Body',
    'NAICS Industry',
    'Nature of Injury',
    'Source',
    'Status'
]

const headerKeys = [
        "accommodation_name",
          "injury_location_name",
          "industry_name",
          "activity_name",
          "verified",
          'status'
]

const headerMap = Object.fromEntries(headers.map((header, index) => [header, headerKeys[index]]));

// Function to get the corresponding header key
export default function getHeaderKey(header) {
    return headerMap[header] || null; // Return the corresponding key or null if not found
};