
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterModule } from '@angular/router';

interface RM {
  name: string;
  employeeId: string;
  team: string;
  region: string;
  visitDate: string;
  visits: number;
  closures: number;
  grossRevenue: number;
  netRevenue: number;
  refundRevenue: number;
}

@Component({
  selector: 'app-rm-performance',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule
  ],
  templateUrl: './rm-performance.component.html',
  styleUrls: ['./rm-performance.component.css']
})
export class RmPerformanceComponent implements OnInit {

  team = 'Seller Team';
  region = 'Chennai';

  searchText = '';
  selectedMonth = '';
  fromDate = '';
  toDate = '';

  // Schedule count (temporary default value)
  totalSchedules: number = 0;

  // Demo records only. Replace with actual Google Sheets data.
  allRMs: RM[] = [
    {
      name: 'Demo RM 1',
      employeeId: 'RM001',
      team: 'Seller Team',
      region: 'Chennai',
      visitDate: '2026-11-05',
      visits: 12,
      closures: 4,
      grossRevenue: 50000,
      netRevenue: 45000,
      refundRevenue: 5000
    },
    {
      name: 'Demo RM 2',
      employeeId: 'RM002',
      team: 'Seller Team',
      region: 'Chennai',
      visitDate: '2026-11-10',
      visits: 15,
      closures: 6,
      grossRevenue: 75000,
      netRevenue: 70000,
      refundRevenue: 5000
    },
    {
      name: 'Demo RM 3',
      employeeId: 'RM003',
      team: 'Seller Team',
      region: 'Chennai',
      visitDate: '2026-10-15',
      visits: 10,
      closures: 3,
      grossRevenue: 35000,
      netRevenue: 30000,
      refundRevenue: 5000
    }
  ];

  filteredRMs: RM[] = [];

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.team = params['team'] || 'Seller Team';
      this.region = params['region'] || 'Chennai';
      this.applyFilters();
    });
  }

  applyFilters(): void {
    this.filteredRMs = this.allRMs.filter(rm => {

      const matchesTeam =
        rm.team === this.team &&
        rm.region === this.region;

      const matchesSearch =
        rm.name.toLowerCase().includes(this.searchText.toLowerCase()) ||
        rm.employeeId.toLowerCase().includes(this.searchText.toLowerCase());

      const matchesMonth =
        !this.selectedMonth ||
        rm.visitDate.startsWith(this.selectedMonth);

      const matchesFromDate =
        !this.fromDate ||
        rm.visitDate >= this.fromDate;

      const matchesToDate =
        !this.toDate ||
        rm.visitDate <= this.toDate;

      return matchesTeam &&
        matchesSearch &&
        matchesMonth &&
        matchesFromDate &&
        matchesToDate;
    });
  }

  get totalVisits(): number {
    return this.filteredRMs.reduce((sum, rm) => sum + rm.visits, 0);
  }

  get totalClosures(): number {
    return this.filteredRMs.reduce((sum, rm) => sum + rm.closures, 0);
  }

  get totalGrossRevenue(): number {
    return this.filteredRMs.reduce((sum, rm) => sum + rm.grossRevenue, 0);
  }

  get totalNetRevenue(): number {
    return this.filteredRMs.reduce((sum, rm) => sum + rm.netRevenue, 0);
  }

  get totalRefunds(): number {
    return this.filteredRMs.reduce((sum, rm) => sum + rm.refundRevenue, 0);
  }

  clearFilters(): void {
    this.searchText = '';
    this.selectedMonth = '';
    this.fromDate = '';
    this.toDate = '';
    this.applyFilters();
  }
}
