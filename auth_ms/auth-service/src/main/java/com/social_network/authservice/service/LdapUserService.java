package com.social_network.authservice.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.ldap.core.LdapClient;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.filter.AndFilter;
import org.springframework.ldap.filter.EqualsFilter;
import org.springframework.stereotype.Service;
import com.social_network.authservice.entity.LdapUser;
import com.social_network.authservice.repository.AuthUserRepository;

@Service
public class LdapUserService {

	@Autowired
	AuthUserRepository authUserRepository;

	@Autowired
	private LdapTemplate ldapTemplate;

	LdapClient ldapClient;

	@Value("${spring.ldap.base}")
	private String ldapBase;

	// Crear un nuevo usuario en LDAP
	public LdapUser createUser(String email, String role, String password) {
		LdapUser finalNewUser = LdapUser.builder().email(email).password(password).build();
		ldapTemplate.bind("cn=" + email + "," + "ou=" + role + "," + ldapBase, null,
				finalNewUser.toAttributes());
		return finalNewUser;
	}

	public boolean authenticate(String email, String password) {
		// Buscar el usuario por correo electrónico
		String ou = authUserRepository.findByEmail(email).get().getRole().name();
		AndFilter filter = new AndFilter();
		filter.and(new EqualsFilter("cn", email));
		String base = "ou=" + ou + "," + ldapBase;
		boolean isLdapUser = ldapTemplate.authenticate(base, filter.toString(), password);
		return isLdapUser;

	}
}
