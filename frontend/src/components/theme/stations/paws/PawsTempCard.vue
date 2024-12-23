<template>
    <div>
      <!-- Station Dropdown -->
      <div class="dropdown mb-4">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="stationDropdown" data-bs-toggle="dropdown" aria-expanded="false">
          Station {{ selectedStation }}
        </button>
        <ul class="dropdown-menu" aria-labelledby="stationDropdown">
          <li v-for="station in station_ids" :key="station">
            <a class="dropdown-item" href="#" @click="changeStation(station)">Station {{ station }}</a>
          </li>
        </ul>
      </div>
  
      <div class="row g-2">
        <!-- Loop through transformed data and display cards for each measurement -->
        <div class="col-xl-3 col-md-6 proorder-xl-3 proorder-md-3" v-for="(item, index) in localPawsData" :key="index">
          <Card1 :cardbodyClass="item.cardclass">
            <div class="d-flex gap-2 align-items-end">
              <div class="flex-grow-1">
                <h2>{{ item.number }}</h2>
                <p class="mb-0 text-truncate">{{ item.text }}</p>
                <div class="d-flex student-arrow text-truncate">
                  <p class="mb-0 up-arrow" :class="item.iconclass"><i :class="item.icon"></i></p>
                  <span class="f-w-500" :class="item.fontclass">{{ item.total }}%</span>{{ item.month }}
                </div>
              </div>
              <div class="flex-shrink-0">
                <img :src="getImages(item.img)" alt="" />
              </div>
            </div>
          </Card1>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted, defineAsyncComponent } from 'vue';
  import axios from 'axios';
  import { getImages } from "@/composables/common/getImages"; // Assuming getImages is a helper function
  
  // Dynamically import the Card1 component
  const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));
  
  // Reactive reference to store transformed data
  const localPawsData = ref([]);
  
  // List of stations to switch between
  const station_ids = [1, 3, 4, 6, 11, 12, 18, 24, 27, 28, 29, 31, 32, 33, 36, 37, 38, 41, 42];
  const selectedStation = ref<number>(station_ids[0]); // Default to the first station in the list
  
  // Helper function to get the unit for each measurement
  const getUnit = (measurementName: string): string => {
      switch (measurementName) {
          case 'BMX280 Pressure': return 'hPa';
          case 'Air Temperature': return '°C';
          case 'Rain Gauge': return 'mm';
          case 'MCP9808 Temperature': return '°C';
          case 'Wind Direction': return '°';
          case 'Wind Speed': return 'm/s';
          default: return '';
      }
  };
  
  // Helper function to get image URL for each measurement
  const getImage = (measurementName: string): string => {
      return 'dashboard-4/icon/student.png';  // Static image URL for demonstration
  };
  
  // Function to transform API data and get the latest measurement for each type
  const transformApiData = (apiData: any[]) => {
      const latestData: { [key: string]: any } = {};
  
      apiData.forEach((item) => {
          if (item.name === `Station ${selectedStation.value}`) {
              const itemTimestamp = new Date(item.timestamp); // Ensure timestamp is a Date object
  
              // Check if this measurement is already stored, and if the current one is newer
              const existingItem = latestData[item.measurement_name];
              if (!existingItem || new Date(existingItem.timestamp) < itemTimestamp) {
                  latestData[item.measurement_name] = {
                      number: `${item.value} ${getUnit(item.measurement_name)}`,
                      text: item.measurement_name,
                      iconclass: item.value > 0 ? "bg-light-success" : "bg-light-danger",
                      icon: item.value > 0 ? "icon-arrow-up font-success" : "icon-arrow-down font-danger",
                      img: getImage(item.measurement_name),
                      cardclass: "student",
                      fontclass: item.value > 0 ? "font-success" : "font-danger",
                      total: Math.abs(item.value).toFixed(1),
                      // Convert to 12-hour format with AM/PM
                      month: itemTimestamp.toLocaleTimeString('en-US', { 
                          hour: '2-digit', 
                          minute: '2-digit', 
                          hour12: true, // 12-hour format
                          timeZone: 'UTC' // Ensure it's in UTC
                      }),
                      timestamp: item.timestamp // Store timestamp for comparison
                  };
              }
          }
      });
  
      return Object.values(latestData);
  };
  
  // Function to fetch data for the selected station
  const fetchData = async () => {
      try {
          const response = await axios.get('http://127.0.0.1:8000/api/Measurements/');
  
          // If the API response is an array, process it and set it to localPawsData
          if (Array.isArray(response.data)) {
              // Transform the data and update the localPawsData reactive reference
              localPawsData.value = transformApiData(response.data);
          } else {
              console.error('API response is not in the expected format');
          }
      } catch (error) {
          console.error('Error fetching station measurements:', error);
      }
  };
  
  // Function to handle station change from the dropdown
  const changeStation = (station: number) => {
      selectedStation.value = station;
      fetchData(); // Fetch new data based on the selected station
  };
  
  // Fetch data initially when the component is mounted
  onMounted(() => {
      fetchData();
  });
  </script>
  
  <style scoped>
  /* Custom styles for the dropdown and cards */
  .instrument-tabs .nav-link.active {
      background-color: #007bff;
      color: white;
  }
  
  .instrument-tabs .nav-item {
      cursor: pointer;
  }
  
  .studay-statistics {
      margin-top: 10px;
  }
  
  .dropdown-menu {
      max-height: 300px; /* Optional: add scroll if there are too many options */
      overflow-y: auto;
  }
  </style>
  