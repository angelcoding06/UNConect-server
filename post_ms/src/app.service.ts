import { Injectable } from '@nestjs/common';
// import { ConfigService } from '@nestjs/config'; // Import ConfigService

@Injectable()
export class AppService {
  // constructor(private configService: ConfigService) {} // Inject ConfigService

  getHello(): string {
    // const databaseName = this.configService.get('MONGO_HOSTNAME'); // Access environment variable
    return `Hello World! Database name is: `;
  }
}
