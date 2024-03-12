package com.social_network.authservice.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

	@Bean
	SecurityFilterChain securityFilterChain(HttpSecurity httpSecurity) throws Exception {
		return httpSecurity.csrf(crsf -> crsf.disable())
				.sessionManagement(
						session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
				.authorizeHttpRequests(authorize -> authorize
						// .requestMatchers(HttpMethod.POST, "/auth/*").permitAll()
						// .requestMatchers(HttpMethod.POST, "/api/v1/books").hasRole("ADMIN")
						// .anyRequest().authenticated())
						.anyRequest().permitAll())
				// .addFilterBefore()
				.build();
	}
}
