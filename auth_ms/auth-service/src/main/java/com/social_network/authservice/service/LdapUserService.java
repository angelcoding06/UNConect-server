package com.social_network.authservice.service;

import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ldap.core.LdapClient;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.filter.AndFilter;
import org.springframework.ldap.filter.EqualsFilter;
import org.springframework.ldap.query.LdapQuery;
import org.springframework.ldap.support.LdapUtils;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import com.social_network.authservice.entity.LdapUser;
import com.social_network.authservice.repository.LdapUserRepository;

@Service
public class LdapUserService {

	@Autowired
	private LdapUserRepository ldapUserRepository;

	@Autowired
	private PasswordEncoder passwordEncoder;

	@Autowired
	private LdapTemplate ldapTemplate;

	LdapClient ldapClient;


	private static final String BASE_DN = "ou=users,dc=unconnect,dc=com";

	// Crear un nuevo usuario en LDAP
	public LdapUser createUser(String email, String password) {
		// String passwordHashed = passwordEncoder.encode(password);
		System.out.println("hashed");
		LdapUser finalNewUser = LdapUser.builder().email(email).password(password).build();
		// finalNewUser.setId(LdapUtils.emptyLdapName());
		System.out.println("aqui");
		// ldapTemplate.authenticate(null, passwordHashed);
		ldapTemplate.bind("cn=" + email + "," + BASE_DN, null, finalNewUser.toAttributes());
		return finalNewUser;
	}

	// // Autenticar un usuario en LDAP
	// public boolean authenticate(String email, String password) {
	// // Buscar el usuario por correo electrónico
	// Optional<LdapUser> user = ldapUserRepository.findByEmail(email);
	// if (!user.isPresent())
	// return false;
	// System.out.println("encontrado");
	// return passwordEncoder.matches(password, user.get().getPassword());
	// }

	public boolean authenticate(String email, String password) {
		// Buscar el usuario por correo electrónico
		String passwordHashed = passwordEncoder.encode(password);
		System.out.println("hashed");
		AndFilter filter = new AndFilter();
		System.out.println(passwordHashed);
		filter.and(new EqualsFilter("cn", email));
		boolean a = ldapTemplate.authenticate(BASE_DN, filter.toString(), password);
		System.out.println(a);
		return a;

	}

	// Actualizar la contraseña de un usuario en LDAP
	public void updatePassword(String email, String newPassword) {
		// Buscar el usuario por correo electrónico
		Optional<LdapUser> user = ldapUserRepository.findByEmail(email);
		if (user.isPresent()) {
			LdapUser finalUser = user.get();
			// Actualizar la contraseña del usuario
			String passwordHashed = passwordEncoder.encode(newPassword);
			finalUser.setPassword(passwordHashed);
			ldapUserRepository.save(finalUser);
		}
	}

	// Eliminar un usuario en LDAP
	public void deleteUser(String email) {
		// Buscar el usuario por correo electrónico
		Optional<LdapUser> user = ldapUserRepository.findByEmail(email);
		if (user.isPresent()) {
			LdapUser finalUser = user.get();
			// Eliminar el usuario de LDAP
			ldapUserRepository.delete(finalUser);
		}
	}
}
