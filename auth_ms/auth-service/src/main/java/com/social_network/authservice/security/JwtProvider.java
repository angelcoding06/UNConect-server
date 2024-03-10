package com.social_network.authservice.security;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.util.Base64;
import java.util.Date;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import com.social_network.authservice.entity.AuthUser;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.annotation.PostConstruct;

@Component
public class JwtProvider {

	@Value("${jwt.secret}")
	private String secret;

	@PostConstruct
	protected void init() {
		secret = Base64.getEncoder().encodeToString(secret.getBytes());
	}

	public String createToken(AuthUser authuser) {
		Map<String, Object> claims;
		claims = Jwts.claims().setSubject(authuser.getEmail());
		claims.put("id", authuser.getId());
		Date now = new Date();
		Date exp = new Date(now.getTime() + 3600000);
		return Jwts.builder().setClaims(claims).setIssuedAt(now).setExpiration(exp)
				.signWith(getSigningKey()).compact();
	}

	public boolean validate(String token) {
		try {
			Jwts.parserBuilder().setSigningKey(getSigningKey()).build().parseClaimsJws(token);
			return true;
		} catch (Exception e) {
			return false;
		}
	}

	public String getEmailFromToken(String token) {
		try {
			return Jwts.parserBuilder().setSigningKey(getSigningKey()).build().parseClaimsJws(token)
					.getBody().getSubject();
		} catch (Exception e) {
			return null;
		}
	}

	private Key getSigningKey() {
		byte[] keyBytes = this.secret.getBytes(StandardCharsets.UTF_8);
		return Keys.hmacShaKeyFor(keyBytes);
	}

}
