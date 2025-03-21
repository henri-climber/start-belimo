
import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Building2, Download, Factory, Gauge, X, CheckSquare, Loader } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Checkbox } from '@/components/ui/checkbox';

// Monthly energy consumption data matching the style in the screenshot
const mockData = [
  { month: 'Jan', value: 2.3, active: false },
  { month: 'Feb', value: 3.1, active: true },
  { month: 'Mar', value: 4.3, active: true },
  { month: 'Apr', value: 3.9, active: false },
  { month: 'May', value: 6.1, active: true },
  { month: 'Jun', value: 6.7, active: true },
];

// List of buildings for multi-select
const availableBuildings = [
  { id: 1, name: 'Headquarters' },
  { id: 2, name: 'Production Facility A' },
  { id: 3, name: 'Production Facility B' },
  { id: 4, name: 'Distribution Center' },
  { id: 5, name: 'Research Lab' },
  { id: 6, name: 'Office Building North' },
  { id: 7, name: 'Office Building South' },
  { id: 8, name: 'Warehouse' },
  { id: 9, name: 'Data Center' },
  { id: 10, name: 'Logistics Hub' },
  { id: 11, name: 'Innovation Center' },
  { id: 12, name: 'Training Facility' },
];

// List of report types
const reportTypes = [
  { id: 1, name: 'ESG Report', description: 'Covers a company\'s Environmental, Social, and Governance performance, focusing on sustainability, ethics, and compliance.' },
  { id: 2, name: 'Sustainability Report', description: 'Provides an overview of environmental impact, energy efficiency, and long-term sustainability goals.' },
  { id: 3, name: 'Corporate Social Responsibility (CSR) Report', description: 'Highlights company initiatives in social responsibility, philanthropy, and ethical business practices.' },
  { id: 4, name: 'Carbon Footprint Report', description: 'Tracks greenhouse gas emissions, energy consumption, and carbon reduction strategies.' },
  { id: 5, name: 'Impact Report', description: 'Evaluates a company\'s broader impact on society and the environment, often linked to sustainability and social responsibility.' },
  { id: 6, name: 'Diversity, Equity, and Inclusion (DEI) Report', description: 'Focuses on workplace diversity, equal opportunity, and inclusion efforts within an organization.' },
];

// Generate years for selection (current year minus 10 to current year)
const generateYearOptions = () => {
  const currentYear = new Date().getFullYear();
  const years = [];
  for (let i = 0; i < 11; i++) {
    years.push(currentYear - i);
  }
  return years;
};

const years = generateYearOptions();

// PDF Report URL
const PDF_REPORT_URL = 'https://firebasestorage.googleapis.com/v0/b/starthack25.firebasestorage.app/o/ESG_Energy_Report.pdf?alt=media&token=b977d24d-43b6-4d07-8414-83f43e104468';

const EnergyDashboard = () => {
  const [companyName] = useState('EcoTech Solutions');
  const [selectedBuildings, setSelectedBuildings] = useState<number[]>([]);
  const [reportYear, setReportYear] = useState<number>(years[0]);
  const [baselineStartYear, setBaselineStartYear] = useState<string>(years[3].toString());
  const [baselineEndYear, setBaselineEndYear] = useState<string>(years[1].toString());
  const [selectedReportType, setSelectedReportType] = useState<string>("1");
  const [liveValues, setLiveValues] = useState(mockData);
  const [totalConsumption, setTotalConsumption] = useState(1284);
  const [isLoading, setIsLoading] = useState(false);
  
  // Animation for "live" data updates
  useEffect(() => {
    const dataInterval = setInterval(() => {
      setLiveValues(prevData => 
        prevData.map(item => ({
          ...item,
          value: item.active ? parseFloat((item.value + (Math.random() * 0.2 - 0.1)).toFixed(1)) : item.value
        }))
      );
    }, 3000);
    
    // Animation to increase total consumption every 5 seconds
    const consumptionInterval = setInterval(() => {
      setTotalConsumption(prev => prev + 1);
    }, 5000);
    
    return () => {
      clearInterval(dataInterval);
      clearInterval(consumptionInterval);
    };
  }, []);

  const handleDownload = () => {
    setIsLoading(true);
    
    // Set a timeout to simulate loading for 3 seconds before opening the PDF
    setTimeout(() => {
      // Open the PDF in a new tab
      window.open(PDF_REPORT_URL, '_blank');
      setIsLoading(false);
      
      console.log('Downloading report...', {
        companyName,
        selectedBuildings,
        reportYear,
        baselineYears: { start: baselineStartYear, end: baselineEndYear },
        reportType: reportTypes.find(type => type.id.toString() === selectedReportType)?.name
      });
    }, 3000);
  };

  const toggleBuildingSelection = (buildingId: number) => {
    setSelectedBuildings(prevSelected => 
      prevSelected.includes(buildingId)
        ? prevSelected.filter(id => id !== buildingId)
        : [...prevSelected, buildingId]
    );
  };

  const selectAllBuildings = () => {
    if (selectedBuildings.length === availableBuildings.length) {
      setSelectedBuildings([]);
    } else {
      setSelectedBuildings(availableBuildings.map(building => building.id));
    }
  };

  const removeBuilding = (buildingId: number) => {
    setSelectedBuildings(prevSelected => 
      prevSelected.filter(id => id !== buildingId)
    );
  };

  const handleYearSliderChange = (value: number[]) => {
    if (value && value.length > 0) {
      const year = value[0];
      setReportYear(year);
      
      // Adjust baseline years if they're greater than or equal to the reporting year
      if (parseInt(baselineStartYear) >= year) {
        setBaselineStartYear((year - 1).toString());
      }
      if (parseInt(baselineEndYear) >= year) {
        setBaselineEndYear((year - 1).toString());
      }
    }
  };

  // Filter years for baseline that are less than the reporting year
  const availableBaselineYears = years.filter(year => year < reportYear);

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="flex justify-between items-center animate-fade-down">
          <div className="space-y-1">
            <h1 className="text-4xl font-bold text-gray-900">{companyName}</h1>
            <p className="text-lg text-gray-600">Monitor and generate ESRS reports based on real-time sensor data</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="p-6 animate-scale-up bg-white border border-gray-100 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <Building2 className="w-6 h-6 text-green-500" />
              </div>
              <div className="text-left">
                <p className="text-sm text-gray-600">Total Buildings</p>
                <p className="text-2xl font-semibold">12</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 animate-scale-up [animation-delay:100ms] bg-white border border-gray-100 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <Gauge className="w-6 h-6 text-green-500" />
              </div>
              <div className="text-left">
                <p className="text-sm text-gray-600">Active Sensors</p>
                <p className="text-2xl font-semibold">284</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 animate-scale-up [animation-delay:200ms] bg-white border border-gray-100 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <Factory className="w-6 h-6 text-green-500" />
              </div>
              <div className="text-left">
                <p className="text-sm text-gray-600">Total Consumption</p>
                <p className="text-2xl font-semibold transition-all duration-1000">{totalConsumption} kWh</p>
              </div>
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="col-span-1 lg:col-span-2 p-6 animate-fade-up bg-white border border-gray-100 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 text-left">Energy Consumption Trend</h2>
            <div className="h-[350px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={liveValues}
                  margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f5f5f5" />
                  <XAxis dataKey="month" axisLine={false} tickLine={false} />
                  <YAxis axisLine={false} tickLine={false} />
                  <Tooltip 
                    cursor={false}
                    contentStyle={{ borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', border: 'none' }}
                  />
                  <Line 
                    type="monotone"
                    dataKey="value" 
                    stroke="#4ade80"
                    strokeWidth={3}
                    dot={false}
                    activeDot={false}
                    animationDuration={1000}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card className="p-6 animate-fade-up [animation-delay:200ms] bg-white border border-gray-100 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 text-left">Report Parameters</h2>
            <div className="space-y-5">
              <div className="space-y-2">
                <Label htmlFor="reportType" className="text-left block">Report Type</Label>
                <Select 
                  value={selectedReportType} 
                  onValueChange={setSelectedReportType}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select report type" />
                  </SelectTrigger>
                  <SelectContent>
                    {reportTypes.map(type => (
                      <SelectItem key={type.id} value={type.id.toString()} className="py-2">
                        {type.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-gray-500 mt-1">
                  {reportTypes.find(type => type.id.toString() === selectedReportType)?.description}
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between mb-1">
                  <Label className="text-left block">Select Buildings</Label>
                  <button 
                    onClick={selectAllBuildings}
                    className="text-sm flex items-center text-green-600 hover:text-green-700"
                  >
                    <CheckSquare className="h-3.5 w-3.5 mr-1" />
                    {selectedBuildings.length === availableBuildings.length ? "Deselect All" : "Select All"}
                  </button>
                </div>
                <div className="flex flex-wrap gap-2 mb-2">
                  {selectedBuildings.map(buildingId => {
                    const building = availableBuildings.find(b => b.id === buildingId);
                    return (
                      <div key={buildingId} className="flex items-center bg-green-50 text-green-700 rounded-full px-3 py-1 text-sm">
                        {building?.name}
                        <button 
                          onClick={() => removeBuilding(buildingId)}
                          className="ml-2 text-green-700 hover:text-green-900"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    );
                  })}
                </div>
                <Select>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Add building" />
                  </SelectTrigger>
                  <SelectContent>
                    {availableBuildings.map(building => (
                      <div key={building.id} className="flex items-center space-x-2 py-1 px-2">
                        <Checkbox 
                          id={`building-${building.id}`} 
                          checked={selectedBuildings.includes(building.id)}
                          onCheckedChange={() => toggleBuildingSelection(building.id)}
                        />
                        <Label 
                          htmlFor={`building-${building.id}`}
                          className="text-sm cursor-pointer flex-1"
                        >
                          {building.name}
                        </Label>
                      </div>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Label className="text-left block">Reporting Year: {reportYear}</Label>
                </div>
                <Slider 
                  defaultValue={[reportYear]} 
                  max={years[0]} 
                  min={years[years.length - 1]} 
                  step={1}
                  onValueChange={handleYearSliderChange}
                  className="py-4"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="baselineStart" className="text-left block">Baseline Start Year</Label>
                  <Select 
                    value={baselineStartYear} 
                    onValueChange={setBaselineStartYear}
                    disabled={availableBaselineYears.length === 0}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Start year" />
                    </SelectTrigger>
                    <SelectContent>
                      {availableBaselineYears.map(year => (
                        <SelectItem 
                          key={year} 
                          value={year.toString()}
                          disabled={parseInt(baselineEndYear) < year}
                        >
                          {year}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="baselineEnd" className="text-left block">Baseline End Year</Label>
                  <Select 
                    value={baselineEndYear} 
                    onValueChange={setBaselineEndYear}
                    disabled={availableBaselineYears.length === 0}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="End year" />
                    </SelectTrigger>
                    <SelectContent>
                      {availableBaselineYears.map(year => (
                        <SelectItem 
                          key={year} 
                          value={year.toString()}
                          disabled={parseInt(baselineStartYear) > year}
                        >
                          {year}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button 
                className="w-full bg-green-500 hover:bg-green-600 text-white transition-all duration-200 ease-in-out transform hover:scale-[1.02]"
                onClick={handleDownload}
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <Loader className="w-4 h-4 mr-2 animate-spin" />
                    Generating Report...
                  </div>
                ) : (
                  <>
                    <Download className="w-4 h-4 mr-2" />
                    Generate Report
                  </>
                )}
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default EnergyDashboard;

