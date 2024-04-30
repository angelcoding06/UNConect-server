package com.social_network.authservice.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.ldap.repository.config.EnableLdapRepositories;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.core.support.LdapContextSource;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
@EnableLdapRepositories
public class SecurityConfig {

	@Value("${spring.ldap.urls}")
	private String ldapUrl;
	@Value("${spring.ldap.username}")
	private String ldapUsername;
	@Value("${spring.ldap.password}")
	private String ldapPassword;

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

	@Bean
	LdapTemplate ldapTemplate() {
		return new LdapTemplate(ContextSource());
	}


	@Bean
	public LdapContextSource ContextSource() {
		LdapContextSource ldapContextSource = new LdapContextSource();
		ldapContextSource.setUrl(ldapUrl);
		ldapContextSource.setUserDn(ldapUsername);
		ldapContextSource.setPassword(ldapPassword);
		return ldapContextSource;
	}

	// @Bean
	// AuthenticationManager authManager(BaseLdapPathContextSource base) {
	// LdapBindAuthenticationManagerFactory factory =
	// new LdapBindAuthenticationManagerFactory(base);
	// factory.setUserDnPatterns("cn={0},ou=users,dc=unconnect,dc=com");
	// return factory.createAuthenticationManager();

	// }
}
