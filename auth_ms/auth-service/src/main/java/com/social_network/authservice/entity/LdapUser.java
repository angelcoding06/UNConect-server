package com.social_network.authservice.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.naming.directory.Attributes;
import javax.naming.directory.BasicAttributes;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LdapUser {

	private String email;

	private String password;

	// standard getters/setters
	public Attributes toAttributes() {
		Attributes attributes = new BasicAttributes();
		attributes.put("ObjectClass", "inetOrgPerson");
		attributes.put("cn", email);
		attributes.put("sn", email);
		attributes.put("userPassword", password);
		return attributes;
	}
}
